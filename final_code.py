from cv2 import cv
import math
import cv2
from time import sleep
posx=0
posy=0
font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
def getthresholdedimg(im):
	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
	'''this function take RGB image.Then convert it into HSV for easy colour detection and threshold it with yellow part as white and all other regions as black.Then return that image'''
	imghsv=cv.CreateImage(cv.GetSize(im),8,3)
	cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)				# Convert image from RGB to HSV
	imgthreshold=cv.CreateImage(cv.GetSize(im),8,1)
	cv.InRangeS(imghsv,cv.Scalar(20,100,100),cv.Scalar(30,255,255),imgthreshold)	# Select a range of yellow color
	return imgthreshold

capture=cv.CaptureFromCAM(0)
sleep(5)
frame = cv.QueryFrame(capture)
frame_size = cv.GetSize(frame)
grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
test=cv.CreateImage(cv.GetSize(frame),8,3)
cv.NamedWindow("Real")
cv.NamedWindow("Threshold")
x1=0
y1=0
x2=0
y2=0

while(1):
	color_image = cv.QueryFrame(capture)
	imdraw=cv.CreateImage(cv.GetSize(frame),8,3)
	cv.Flip(color_image,color_image,1)
	cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
	imgyellowthresh=getthresholdedimg(color_image)
	cv.Erode(imgyellowthresh,imgyellowthresh,None,3)
	cv.Dilate(imgyellowthresh,imgyellowthresh,None,10)

	storage = cv.CreateMemStorage(0)
	imgyellowthresh1=cv.GetMat(imgyellowthresh)
	imgyellowthresh2=cv.GetMat(imgyellowthresh)
	moments1=cv.Moments(imgyellowthresh1,0)
	area1=cv.GetCentralMoment(moments1,0,0)
	moments2=cv.Moments(imgyellowthresh2,0)
	area2=cv.GetCentralMoment(moments2,0,0)
	contour = cv.FindContours(imgyellowthresh, storage, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)
	points = []	
#	This is the new part here. ie Use of cv.BoundingRect()
#	while contour:
	print"here"
	#print posx
	#print posy
	# Draw bounding rectangles
	'''if contour!=None and contour.h_next()!=None:
		contour=contour.h_next()[0]
		print contour.h_next()[0]'''
	# for more details about cv.BoundingRect,see documentation
	'''pt1 = (bound_rect[0], bound_rect[1])
	print pt1
	#print pt1
	pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
	print pt2'''
	#points.append(pt1)
	#points.append(pt2)
	#cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)
	'''lastx=posx #lastx = 0 / 
	lasty=posy #lasty = 0 / 
	posx=cv.Round((pt1[0]+pt2[0])/2) 
	posy=cv.Round((pt1[1]+pt2[1])/2)  
	if lastx!=0 and lasty!=0:
		cv.Line(imdraw,(posx,posy),(lastx,lasty),(0,255,255))
		cv.Circle(imdraw,(posx,posy),5,(0,255,255),-1)'''
	if (area1 >200000):
		#x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
		x1=int(cv.GetSpatialMoment(moments1,1,0)/area1)
		y1=int(cv.GetSpatialMoment(moments1,0,1)/area1)
		#draw circle
		cv.Circle(imdraw,(x1,y1),2,(0,255,0),20)
		#write x and y position
		cv.PutText(imdraw,str(x1)+","+str(y1),(x1,y1+20),font, 255)
		#Draw the text
	if (area2 >100000):
		#x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
		x2=int(cv.GetSpatialMoment(moments2,1,0)/area2)
		y2=int(cv.GetSpatialMoment(moments2,0,1)/area2)
		#draw circle
		cv.Circle(imdraw,(x2,y2),2,(0,255,0),20)
		cv.PutText(imdraw,str(x2)+","+str(y2),(x2,y2+20),font, 255) #Draw the text
		cv.Line(imdraw,(x1,y1),(x2,y2),(0,255,0),4,cv.CV_AA)
		cv.Line(imdraw,(x1,y1),(cv.GetSize(img)[0],y1),(100,100,100,100),4,cv.CV_AA)
	x1=float(x1)
	y1=float(y1)
	x2=float(x2)
	y2=float(y2)
	if x2-x1!=0:
		angle=int(math.atan((y1-y2)/(x2-x1))*180/math.pi)
		cv.PutText(imdraw,str(angle),(int(x1)+50,(int(y2)+int(y1))/2,font,255))
	cv.Add(test,imdraw,test)
	cv.ShowImage("Real",color_image)
	cv.ShowImage("Threshold",test)