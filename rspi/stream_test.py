import cv2
import time

cap = cv2.VideoCapture("rtsp://crtlabs:Abudabu1!@430n.crtlabs.org:554/videoMain")
#cap = cv2.VideoCapture("flow.mp4")
while(1):
	ret, frame = cap.read()
	if ret == True:
		cv2.imshow("test", frame)
	key = cv2.waitKey(10)
