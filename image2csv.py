from tools import draw_region
from tools import region_creator
from tools import pre_process
from tools import to_matrix
import numpy as np
import argparse
import cv2
import pytesseract
import logging
import time

logging.getLogger().setLevel(logging.INFO)

# internal parameters to resize the region before giving it to Tesseract
window_maximizer = 6

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, type=str, help="path to input image")
ap.add_argument("-p", "--path", default="./", type=str, help="path to output .csv file")
ap.add_argument(
    "-g",
    "--grid",
    default=False,
    type=str,
    help="True to select manually the boxes of the images",
)
ap.add_argument(
    "-v",
    "--visualization",
    default="n",
    type=str,
    help="y/[n] to see each extracted regions individualy",
)
ap.add_argument(
    "-m",
    "--method",
    type=str,
    default="fast",
    help="[fast]/denoize method to pre-process regions of the input image",
)
args = vars(ap.parse_args())

visu = args["visualization"]

start = time.time()
logging.info("Beginning of the script...")

# load the input image from disk
logging.info("Loading of grayscale image...")
image = cv2.imread(args["image"])

# create regions to be scanned
logging.info("Extracting regions...")

if args["grid"]:  # use manual grid detection
    boxes = [draw_region(image)]
    boxes, grid_shape = region_creator(image, boxes)
else:  # by default, perform automatic grid detection
    from grid_detector import detect_grid

    boxes, grid_shape = detect_grid(image)

ROI = []
for i in range(len(boxes)):
    X1 = boxes[i][0][0]
    X2 = boxes[i][1][0]
    Y1 = boxes[i][0][1]
    Y2 = boxes[i][1][1]
    roi = image[Y1:Y2, X1:X2]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    (h, w) = roi.shape[:2]
    roi = cv2.resize(
        roi, (w * window_maximizer, h * window_maximizer), interpolation=cv2.INTER_CUBIC
    )
    ROI.append(roi)

# Preprocessing the images
logging.info(f"""Pre-processing the regions with method {args["method"]}...""")
ROI = pre_process(ROI, visu, args["method"])

# Give regions to machine learning model in order to be classified
logging.info(f"Applying OCR to the regions...")
custom_config = r"--oem 0 --psm 6"
# see Tesseract's documentation for more info (command line: $ tesseract --help-oem ; $ tesseract --help-psm)
numbers = []
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\User\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
NbError = 0
for i in range(len(ROI)):
    region = ROI[i]
    
    number = pytesseract.image_to_string(region, config=custom_config)

    # test if the string can be casted into float
    isInt = True
    try:
        number = float(number)
    except ValueError:
        isInt = False

    # if the detection cannot be casted, it is an error
    if not isInt:
        number = float("inf")
        NbError += 1
        numbers.append(number)
    else:
        numbers.append(number)

    # draw a progress line
    progress_line = ""

    for p in range(30):
        if p <= int((i + 1) / len(ROI) * 30):
            progress_line += "="
        else:
            progress_line += "."

    print(f"{i + 1}/{len(ROI)} [{progress_line}]", end="\r", flush=True)

    # if wanted, show the extracted region and print the detection in the terminal
    if visu == "y":
        print("\n")
        print("-----------------------------")
        cv2.imshow("region proceeded (press 0 to close)", region)
        print("res = ", number)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

print("")
logging.info(f"End of OCR, found {NbError} errors out of {len(ROI)} regions...")

# Exporting the results
logging.info(f"""Exporting to path {args["path"]}...""")

out = to_matrix(numbers, grid_shape[0], grid_shape[1])

np.savetxt(args["path"] + "output.csv", out, delimiter=",", fmt="%10.3f")

logging.info(f"Ending of the script within {round(time.time()-start, 2)} seconds.")