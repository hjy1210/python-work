# import the necessary packages
import argparse
import cv2

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []

status="normal"
width=1920
height=768
imageW=0
imageH=0
top=0
left=0
rois=[]
def constraintAdd(val,inc,max):
	v=val+inc
	if v<0:
		v=0
	if v>max:
		v=max
	return v
def viewportImage(top,left):
	img=curImage.copy()
	return img[top:(top+height),left:(left+width)]
def getCurImage():
	tmpImage=image.copy()
	for roi in rois:
		cv2.rectangle(tmpImage,roi[0],roi[1],(0,0,255),2)
	return tmpImage
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, img, top, left, status, rois, curImage

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		if flags==9:  # ctrl + leftbuttondown
			status="cropping"
		elif flags==1: # pure leftbuttondown
			status="moving"
		else:
			status="normal"
		refPt = [(x, y)]

		# cropping = True
		#print(flags,param)

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		if (len(refPt)==1):
			refPt.append((x, y))
		elif (len(refPt)==2):
			refPt[1]=(x,y)
		if status=="cropping":
			# draw a rectangle around the region of interest
			#cv2.rectangle(img, refPt[0], refPt[1], (0, 255, 0), 2)
			newroi=((left+refPt[0][0],top+refPt[0][1]),(left+refPt[1][0],top+refPt[1][1]))
			rois.append(newroi)
			curImage=getCurImage()
			img=viewportImage(top,left)
			cv2.imshow("image", img)
			print(rois)
		elif status=="moving":
			top=constraintAdd(top,refPt[0][1]-refPt[1][1],imageH-height)
			left= constraintAdd(left,refPt[0][0]-refPt[1][0],imageW-width)
			#img=curImage.copy()
			#img=image[top:(top+height),left:(left+width)]
			img=viewportImage(top,left)
			cv2.imshow("image", img)
		status="normal"
		refPt=[]

	elif event == cv2.EVENT_MOUSEMOVE:
		if (len(refPt)==1):
			refPt.append((x, y))
		elif (len(refPt)==2):
			refPt[1]=(x,y)
		else:
			return
		if status=="moving":
			top1=constraintAdd(top,refPt[0][1]-refPt[1][1],imageH-height)
			left1= constraintAdd(left,refPt[0][0]-refPt[1][0],imageW-width)
			#img=curImage.copy()
			#img=img[top1:(top1+height),left1:(left1+width)]
			img=viewportImage(top1,left1)
			# print(top1,left1)
			cv2.imshow("image",img)
		elif status=="cropping":
			# roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
			#img= curImage.copy()
			#img=img[top:(top+height),left:(left+width)]
			img=viewportImage(top,left)
			cv2.rectangle(img,refPt[0],refPt[1],(0,255,255),1)
			cv2.imshow("image", img)
        

        
"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
"""
image = cv2.imread('opencv/data/9-302-203-29-1-1-1.jpg')
imageH=image.shape[0]
imageW=image.shape[1]
curImage = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
img=viewportImage(top,left)
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", img)
	key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		img = curImage.copy()
		refPy=[]

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

# if there are two reference points, then crop the region of interest
# from teh image and display it
#if len(refPt) == 2:
#	roi = curImage[(top+refPt[0][1]):(top+refPt[1][1]), (left+refPt[0][0]):(left+refPt[1][0])]
#	cv2.imshow("ROI", roi)
#	cv2.waitKey(0)
r=width/curImage.shape[1]
h=int(r*curImage.shape[0])
img=cv2.resize(curImage,(width,h))
cv2.imshow("image", curImage)
cv2.waitKey(0)
i=0
for roi in rois:
	i=i+1
	tmpimg=image[roi[0][1]:roi[1][1],roi[0][0]:roi[1][0]]
	name= "opencv/data/template-{}.jpg".format(i)
	cv2.imwrite(name,tmpimg)

# close all open windows
cv2.destroyAllWindows()
