#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:02:19 2020

@author: Reaz
"""
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--prototxt", required=True,
#	help="path to Caffe 'deploy' prototxt file")
#ap.add_argument("-m", "--model", required=True,
#	help="path to Caffe pre-trained model")
#ap.add_argument("-c", "--confidence", type=float, default=0.2,
#	help="minimum probability to filter weak detections")
#ap.add_argument("-mW", "--montageW", required=True, type=int,
	#help="montage frame width")
#ap.add_argument("-mH", "--montageH", required=True, type=int,
	#help="montage frame height")
args = vars(ap.parse_args())

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()

# initialize the dictionary which will contain  information regarding
# when a device was last active, then store the last time the check
# was made was now
frameDict = {}

lastActive = {}
lastActiveCheck = datetime.now() 


# stores the estimated number of Pis, active checking period, and
# calculates the duration seconds to wait before making a check to
# see if a device was active
ESTIMATED_NUM_PIS = 1
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

# assign montage width and height so we can view all incoming frames# in a single "dashboard"
mW = 1
mH = 1



while True:
	# receive RPi name and frame from the RPi and acknowledge
	# the receipt
	(rpiName, frame) = imageHub.recv_image()       
	imageHub.send_reply(b'OK')  
    
    # if a device is not in the last active dictionary then it means
	# that its a newly connected device
	if rpiName not in lastActive.keys():
		print("[INFO] receiving data from {}...".format(rpiName))

	# record the last active time for the device from which we just
	# received a frame

	lastActive[rpiName] = datetime.now()

    # resize the frame to have a maximum width of 400 pixels, then
	# grab the frame dimensions and construct a blob 
	#print ('BEFORE BLOB')
	frame = imutils.resize(frame, height=1200, width=600)
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (700, 700)),
		0.007843, (400, 400), 127.5)  
	#print ('AFTER BLOB')
    
    
    ### skipping all object detection stuff
    
    # draw the sending device name on the frame
	cv2.putText(frame, rpiName, (10, 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



    # update the new frame in the frame dictionary
	frameDict[rpiName] = frame 
    
    # build a montage using images in the frame dictionary
	montages = build_montages(frameDict.values(), (w, h), (mW, mH)) 
    
	
    # display the montage(s) on the screen
	for (i, montage) in enumerate(montages):
		cv2.imshow("Home pet location monitor ({})".format(i),
			montage) 
	#print ('Montages are displaying')    

    # detect any kepresses
	key = cv2.waitKey(1) & 0xFF 
    
    # if current time *minus* last time when the active device check
	# was made is greater than the threshold set then do a check
	if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
		# loop over all previously active devices
		for (rpiName, ts) in list(lastActive.items()):
			# remove the RPi from the last active and frame
			# dictionaries if the device hasn't been active recently
			if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
				print("[INFO] lost connection to {}".format(rpiName))
				lastActive.pop(rpiName)
				frameDict.pop(rpiName)

		# set the last active check time as current time
		lastActiveCheck = datetime.now()

	#print ('if loop finished')
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()










