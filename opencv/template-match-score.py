import os,sys
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import json

"""
summary: get cvImage from file
file: path of image file, path may contain non-ascii characters
mod: imageMode, 0 is gray, 1 is color
return cvImage
"""
def getCvImage(file,mode):
    stream = open(file, "rb")
    bytes = bytearray(stream.read())
    numpyarray = np.asarray(bytes, dtype=np.uint8)
    bgrImage = cv.imdecode(numpyarray,mode)
    return(bgrImage)
"""
summary: save img to file
file: path of image file, path may contain non-ascii characters
img: cvImage
"""
def saveCvImage(img,file):
    ext=file[file.rfind("."):]
    ret,buffer = cv.imencode(ext, img)
    stream = open(file, "wb")
    stream.write(buffer)
"""
summary: use templatefile as template to do template-match with imgfile
display top-left of match location with confidence
"""
def match(imgfile,templatefile,display=False):
    # img and template should be on the sample scale
    # img = cv.imread('opencv/messi5.jpg',0)
    #img = cv.imread(imgfile,0)
    img = getCvImage(imgfile,0)
    img2 = img.copy()
    """
    relative path is relative to root directory of workspace
    """
    # template = cv.imread('opencv/template5.png',0)
    #template = cv.imread(templatefile,0)
    template = getCvImage(templatefile,0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    meth= methods[1]
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
        value = min_val
    else:
        top_left = max_loc
        value = max_val
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 0, 2)
    if display:
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()
    return top_left, value
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
        'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
#meth= methods[1]
#img = img2.copy()
#method = eval(meth)

# img and template should be on the sample scale
def perfomeMatch(img,template,method,display=False):
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
        value = min_val
    else:
        top_left = max_loc
        value = max_val
    bottom_right = (top_left[0] + w, top_left[1] + h)
    if display:
        img2=img.copy()
        cv.rectangle(img2,top_left, bottom_right, 0, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img2,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        #plt.suptitle(str(method))
        plt.show()
    return top_left, value


rootdir='d:/20181205錱俞提供/01國文/卷1'
#templatefile='opencv/data/ch10-15.png'
jsonfile='opencv/data/ch-template-2.json'
jsonImageFile='opencv/data/9-302-203-29-1-1-1.jpg'
templateImage=getCvImage(jsonImageFile,0)
with open(jsonfile, "r") as read_file:
    templateData=json.load(read_file)
lt=templateData[0]["lt"]
rb=templateData[0]["rb"]
template=templateImage[lt[1]:rb[1],lt[0]:rb[0]]
#plt.imshow(template)
#plt.show()
print(template.shape)
#templatefile='opencv/data/template-3.jpg'
#template = getCvImage(templatefile,0)
method = eval(methods[1])
print(template.shape)
w=template.shape[1]
h=template.shape[0]
label="ABCDEFGH"
count=11
output=np.zeros((h*count,w),dtype=np.uint8)
i=0
def secondRun(rootdir,display):
    global i
    for f in os.listdir(rootdir):
        fn=os.path.join(rootdir,f)
        if os.path.isfile(fn) and (fn.endswith(".png") or fn.endswith(".jpg")):
            try:
                img=getCvImage(fn,0)
                res=perfomeMatch(img,template,method,display)
                cv.rectangle(img,(res[0][0],res[0][1]),(res[0][0]+w,res[0][1]+h),0,2)
                s=f+"@"
                for child in templateData[0]["children"]:
                    if "type" in child.keys() and child["type"]=="sequence":
                        s=s+" "+child["name"]+":"
                        cx=child["start"][0]
                        cy=child["start"][1]
                        stepx=(child["end"][0]-cx)/(child["count"]-1)
                        stepy=(child["end"][1]-cy)/(child["count"]-1)
                        w1=child["width"]
                        h1=child["height"]
                        for ndx in range(child["count"]):
                            cury=res[0][1]-lt[1]+(cy-h1//2)+int(ndx*stepy)
                            curx=res[0][0]-lt[0]+(cx-w1//2)+int(ndx*stepx)
                            #print(curx,cury,w1,h1)
                            tot=sum(sum(img[cury:(cury+h1),curx:(curx+w1)]<128))
                            if tot>180:
                                s=s+label[ndx]
                            cv.rectangle(img,(curx,cury),(curx+w1,cury+h1),0,2)
                print(s)
                plt.imshow(img)
                plt.show()

            except:
                print(f, sys.exc_info()[0], "*******************")
        if os.path.isdir(fn):
            secondRun(fn,display)

secondRun(rootdir, False)
#cv.imwrite("opencv/data/output.jpg",output)