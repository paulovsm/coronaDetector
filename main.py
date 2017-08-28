import cv2
import sys, getopt
import numpy as np
import csv
from coronaDetector import detector
from numpy import interp

myopts, args = getopt.getopt(sys.argv[1:],"f:s:")

inputFile=''
inputFileName=''
sensitivity=0


# function to convert floating point number of seconds to 
# hh:mm:ss.sss
def secondsToStr(t):
    return "%02d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

for o, a in myopts:
    if o == '-f':
        inputFile = a
        inputFileName = a[:-4]
        print inputFileName
    elif o == '-s':
        sensitivity = a
    else:
        print("Usage: %s -f file -s sensitivity" % sys.argv[0])

if inputFile == "" :
	print ("Video file not informed.")
	sys.exit(0) 

if sensitivity == "" : 
	print ("Sensitivity not informed. Using default configuration")
	sensitivity = 60
else:
	sensitivity = int(sensitivity)

sensitivity = interp(sensitivity, [0,100], [255,0])

cap = cv2.VideoCapture("/videos/input/" + inputFile);

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if int(major_ver)  < 3 :
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
else :
    fps = cap.get(cv2.CAP_PROP_FPS)
    print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_full = cv2.VideoWriter("/videos/output/" + inputFileName + '_complete.avi',fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
shrink_full = cv2.VideoWriter("/videos/output/" + inputFileName + '_small.avi',fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

frame_counter = 0
rois = []

while(cap.isOpened()):
	frame_counter = frame_counter+1
	ret, frame = cap.read()

	if (ret):
		#r = 640.0 / frame.shape[1]
		#dim = (640, int(frame.shape[0] * r))
		#resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
		detection,roi = detector.detectCorona(frame, frame_counter, fps, sensitivity)

		if len(roi) > 0:
			#rois.append(roi)
			cv2.rectangle(detection,(roi[0],roi[1]),(roi[0] + roi[2], roi[1] + roi[3]),(0,0,255),1)
			shrink_full.write(detection)
			with open("/videos/output/" + inputFileName + '.csv', 'a+') as csvfile:
				csv_writer = csv.writer(csvfile)
				csv_writer.writerow([frame_counter, secondsToStr(frame_counter/fps)])

		out_full.write(detection)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break

cap.release()
out_full.release()
shrink_full.release()
