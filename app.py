# %% q불러오기
from PIL import Image
import numpy as np
import cv2

img_file = 'table.jpg'
src = cv2.imread(img_file)

# %% 뭐지
# https://076923.github.io/posts/Python-opencv-28/


dst = src.copy()
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 1500, 1000, apertureSize = 5, L2gradient = True)
# canny = cv2.Canny(gray, 1000, 1, apertureSize = 5, L2gradient = True)

# %%  라인
# lines = cv2.HoughLines(canny, 0.8, np.pi / 180, 150, srn = 0, stn = 0, min_theta = 0, max_theta = np.pi)
lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 90, minLineLength = 10, maxLineGap = 100)
# %% 보이기
cv2.imshow("dst",canny)
cv2.waitKey(0)
cv2.destroyAllWindows()

# %% 그림 그리는거인듯
cnt = 0
for i in lines:
    # length__ = ((i[0][0]-i[0][2])**2+(i[0][1]-i[0][3])**2)**0.5
    # print(length__)
    if cnt < 100: cnt+=1
    else: break
    cv2.line(dst, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 1)


print(set(cnt))
# %%

cv2.imshow("dst", canny)
cv2.waitKey(0)
cv2.destroyAllWindows()
# %%

# %%
