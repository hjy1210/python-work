import sys
import os
from PIL import Image, ExifTags
import numpy as np
import cv2
from matplotlib import pyplot as plt
"""
opencv deep learning demo 程式與相關資料在 https://github.com/spmallick/learnopencv/tree/master/FaceDetectionComparison
"""

"""
使用 PIL 有兩個功能。
其一，它可以接受檔案路徑有中文(unicode chars)。
其二，它可以擷取照片是否旋轉的訊息，將照片轉正。
這兩者都是 opencv 所沒有的功能。
"""
#rootdir = "d:/downloads/errorposition中文/raw"
rootdir = "d:/downloads/test_sat"
#rootdir = "d:/20181205錱俞提供/01國文/卷1"
dic_exif = {
    1: 0,
    8: 90,
    3: 180,
    6: -90
}

def detectFaceOpenCVDnn(net, frame):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    # bb 代表信心指數最高的框框
    bb =None
    maxConf=0
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            if bb==None or confidence>maxConf:
                bb=[x1, y1, x2, y2]
                maxConf=confidence
            bboxes.append([x1, y1, x2, y2])
    if not bb==None:
        cv2.rectangle(frameOpencvDnn, (bb[0],bb[1]),(bb[2],bb[3]), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

# dnn 設定
DNN = "TF"
if DNN == "CAFFE":
    modelFile = "opencv/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    configFile = "opencv/models/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
else:
    modelFile = "opencv/models/opencv_face_detector_uint8.pb"
    configFile = "opencv/models/opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
conf_threshold = 0.7

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
    #  exif.keys()可能沒有沒有'Orientation'
    if not 'Orientation' in exif.keys():
        exif['Orientation']=1
    # exif['Orientation'] 除了1,8,3,6外萬一還有其他值
    try:
        degree = dic_exif[exif['Orientation']]
    except:
        degree = 0
        print(exif['Orientation'])
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
    # 用 dnn 進行辨識
    img, dets = detectFaceOpenCVDnn(net,img)
    print("Number of faces detected: {}".format(len(dets)))

    # matplot 接受的是 RGB 格式
    plt.imshow(img[:,:,::-1])
    plt.show()

