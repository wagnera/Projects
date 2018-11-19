
import cv2
import time

cap = cv2.VideoCapture('rtsp://user:abc123abc@192.168.128.131/axis-media/media.amp')
base_filename='/home/anthony/capture/axis_cal_01_'
counter=0
wait = raw_input("PRESS ENTER TO START.")
while 1:
	if cap.isOpened(): #make sure video capture object is open
		for i in range(10):#empty buffer
			cap.grab()
		ret, frame = cap.read() #read frame from device
		filename=base_filename+str(counter)+'.bmp'
		cv2.imwrite(filename,frame)
		print("wrote to file: " + filename)
		cv2.imshow('frame',frame)
		cv2.waitKey(1)
		time.sleep(1)
		counter+=1