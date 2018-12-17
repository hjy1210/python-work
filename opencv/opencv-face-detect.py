import sys
import os
from PIL import Image, ExifTags
import numpy as np
import cv2
from matplotlib import pyplot as plt

"""
使用 PIL 有兩個功能。
其一，它可以接受檔案路徑有中文(unicode chars)。
其二，它可以擷取照片是否旋轉的訊息，將照片轉正。
這兩者都是 opencv 所沒有的功能。
"""
rootdir = "d:/downloads/errorposition中文/raw"
#rootdir = "d:/tmp"
#rootdir = "d:/20181205錱俞提供/01國文/卷1"
dic_exif = {
    1: 0,
    8: 90,
    3: 180,
    6: -90
}

faceCascade = cv2.CascadeClassifier('opencv/data/lbpcascades/lbpcascade_frontalface_improved.xml')

for filename in os.listdir(rootdir):  # sys.argv[1:]:
    if not filename.lower().endswith(".jpg"):
        continue

    fn = os.path.join(rootdir, filename)
    print("Processing file: {}".format(fn))
    img = Image.open(fn)
    try:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
    except:
        exif = {
            'Orientation': 1
        }
    degree = dic_exif[exif['Orientation']]
    # 圖片選轉 ， expand 要設定 (不然旋轉後會有黑邊)
    if not degree==0:
        img = img.rotate(degree, expand=1)
    # 轉換成 opencv image
    img = np.array(img) 
    # Convert RGB to BGR 
    img = img[:, :, ::-1].copy() 
    # 寬度太大加以調整為1024，太大會造成速度太慢甚至辨認不出人臉
    if img.shape[1]>1024:
        ratio=1024/img.shape[1]
        dim=(1024,int(img.shape[0]*ratio))
        img=cv2.resize(img,dim)
    # 用 lbpcascade_frontalface_improved.xml 進行辨識
    dets = faceCascade.detectMultiScale(img)
    print("Number of faces detected: {}".format(len(dets)))
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".
            format(i, d[0],d[1],d[0]+d[2],d[1]+d[3]))
    for det in dets:
        cv2.rectangle(img,(det[0],det[1]),(d[0]+d[2],d[1]+d[3]),0,2)
    # matplot 接受的是 RGB 格式
    plt.imshow(img[:,:,::-1])
    plt.show()

