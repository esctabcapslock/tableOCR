# %% 임폴트
import pytesseract
from PIL import Image

image  = Image.open('./table.jpg')
#path to tesseract-ocr
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\User\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


# %%
text=(pytesseract.image_to_string(image))
# %%
