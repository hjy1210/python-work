import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('opencv/data/messi5.jpg',0)    # cv::IMREAD_GRAYSCALE = 0, cv::IMREAD_COLOR = 1, 
rows,cols = img.shape[:2]

M = cv2.getRotationMatrix2D((cols/2,rows/2),3,1)
dst = cv2.warpAffine(img,M,(cols,rows))

plt.subplot(121),plt.imshow(img)
plt.title('original'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst)
plt.title('after rotate'), plt.xticks([]), plt.yticks([])
plt.suptitle("Rotation")
plt.show()