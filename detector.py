import cv2
import numpy as np
import math

AREA_MIN = 50
GREEN = [0,255,0]
BLUE = [255,0,0]

def channel_processing(channel):
    pass
    channel = cv2.adaptiveThreshold(channel, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 55, 7)
    #mop up the dirt
    channel = cv2.dilate(channel, None, 1)
    channel = cv2.erode(channel, None, 1)


def detectCorona (frame, frameNumber, FPS, sensitivity):
	output = frame.copy()

	#convert frame to monochrome and blur
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (9,9), 0)
 
    #use function to identify threshold intensities and locations
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
 
    #threshold the blurred frame accordingly
	hi, threshold = cv2.threshold(blur, maxVal-sensitivity, 240, cv2.THRESH_BINARY)
	threshold = cv2.erode(threshold, (3,3), iterations = 3)

	#edged = cv2.Canny(threshold, 50, 150)
	edged = cv2.Canny(threshold, 5, 70, 3)

	ret, lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	biggestContour = None
	boundingRect = []
	biggestContourArea = 0

	for c in lightcontours:
		x,y,w,h = cv2.boundingRect(c)
		area = cv2.contourArea(c)
		radius = w / 2
		#perim = 2*w + 2*h
		perim = cv2.arcLength(c, True)
		if perim > 0:
			T = 4*math.pi * (area/math.pow(perim,2))

			if cv2.contourArea(c) > AREA_MIN and T > 0.85:
				cv2.drawContours(output,[c],0,BLUE,1)

			if biggestContour is None:
				biggestContour = c
			elif cv2.contourArea(biggestContour) < area and T > 0.85:
				biggestContour = c

	if cv2.contourArea(biggestContour) > AREA_MIN:
		cv2.drawContours(output,[biggestContour],0,GREEN,2)
		x1,y1,w1,h1 = cv2.boundingRect(biggestContour)
		boundingRect.append(x1)
		boundingRect.append(y1)
		boundingRect.append(w1)
		boundingRect.append(h1)
		boundingRect.append(frameNumber/FPS)
		boundingRect.append(biggestContourArea)
		boundingRect.append(output)

	return output, boundingRect
