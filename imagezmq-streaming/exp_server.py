#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:46:01 2020

@author: Reaz
"""

# USAGE
# python server.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --montageW 2 --montageH 2

# import the necessary packages
from imutils import build_montages
#from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2 
import datetime 

def main(prototxt,model):
    # construct the argument parser and parse the arguments
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-p", "--prototxt",required=True,
    	#help="path to Caffe 'deploy' prototxt file")
    #ap.add_argument("-m", "--model", required=True,
    	#help="path to Caffe pre-trained model")
#    ap.add_argument("-c", "--confidence", type=float, default=0.2,
#    	help="minimum probability to filter weak detections")
#    ap.add_argument("-mW", "--montageW", default=1, type=int,
#    	help="montage frame width")
#    ap.add_argument("-mH", "--montageH", default=1, type=int,
#    	help="montage frame height")
#    args = vars(ap.parse_args())
    
    # initialize the ImageHub object
    imageHub = imagezmq.ImageHub()
    
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    	"sofa", "train", "tvmonitor"]
    
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    
    # initialize the consider set (class labels we care about and want
    # to count), the object count dictionary, and the frame  dictionary
    #CONSIDER = set(["dog", "person", "car"]) 
    CONSIDER = set(["person"])
    objCount = {obj: 0 for obj in CONSIDER} 
    
    frameDict = {}
    
    # initialize the dictionary which will contain  information regarding
    # when a device was last active, then store the last time the check
    # was made was now
    lastActive = {}
    lastActiveCheck = datetime.datetime.now()
    
    # stores the estimated number of Pis, active checking period, and
    # calculates the duration seconds to wait before making a check to
    # see if a device was active
    ESTIMATED_NUM_PIS = 4
    ACTIVE_CHECK_PERIOD = 10
    ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD
    
    # assign montage width and height so we can view all incoming frames
    # in a single "dashboard"
    mW = 1
    mH = 1
    print("[INFO] detecting: {}...".format(", ".join(obj for obj in
    	CONSIDER)))
    
    # start looping over all the frames
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
    	lastActive[rpiName] = datetime.datetime.now() 
    	timestamp = datetime.datetime.now()    
        
    	# resize the frame to have a maximum width of 400 pixels, then
    	# grab the frame dimensions and construct a blob
    	frame = imutils.resize(frame, width=700) 
    	cv2.putText(frame, timestamp.strftime(
    			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
    			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    	(h, w) = frame.shape[:2] 
    	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
    		0.007843, (300, 300), 127.5)
    
    	# pass the blob through the network and obtain the detections and
    	# predictions
    	net.setInput(blob)
    	detections = net.forward()
    
    	# reset the object count for each object in the CONSIDER set
    	objCount = {obj: 0 for obj in CONSIDER}
    
        
        # loop over the detections
    	for i in np.arange(0, detections.shape[2]):
    		# extract the confidence (i.e., probability) associated with
    		# the prediction
    		confidence = detections[0, 0, i, 2]
    
    		# filter out weak detections by ensuring the confidence is
    		# greater than the minimum confidence
    		if confidence > 0.2:
    			# extract the index of the class label from the
    			# detections
    			idx = int(detections[0, 0, i, 1])
    
    			# check to see if the predicted class is in the set of
    			# classes that need to be considered
    			if CLASSES[idx] in CONSIDER:
    				# increment the count of the particular object
    				# detected in the frame
    				objCount[CLASSES[idx]] += 1 
    				#print (objCount['person'])
    
    				# compute the (x, y)-coordinates of the bounding box
    				# for the object
    				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
    				(startX, startY, endX, endY) = box.astype("int")
    
    				# draw the bounding box around the detected object on
    				# the frame
    				cv2.rectangle(frame, (startX, startY), (endX, endY),
    					(255, 0, 0), 2)
    
    	# draw the sending device name on the frame
    	cv2.putText(frame, rpiName, (10, 25),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    	# draw the object count on the frame
    	label = ", ".join("{}: {}".format(obj, count) for (obj, count) in
    		objCount.items())
    	
    
    	# update the new frame in the frame dictionary
    	frameDict[rpiName] = frame 
    	
    
    	# build a montage using images in the frame dictionary
    	montages = build_montages(frameDict.values(), (w, h), (mW, mH))
    
    	# display the montage(s) on the screen
#    	for (i, montage) in enumerate(montages):
#    		cv2.imshow("Home Security Monitor ({})".format(i),
#    			montage)
    	return frame 
    
    	# detect any kepresses
    	key = cv2.waitKey(1) & 0xFF
    
    	# if current time *minus* last time when the active device check
    	# was made is greater than the threshold set then do a check
    	if (datetime.datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
    		# loop over all previously active devices
    		for (rpiName, ts) in list(lastActive.items()):
    			# remove the RPi from the last active and frame
    			# dictionaries if the device hasn't been active recently
    			if (datetime.datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
    				print("[INFO] lost connection to {}".format(rpiName))
    				lastActive.pop(rpiName)
    				frameDict.pop(rpiName)
    
    		# set the last active check time as current time
    		lastActiveCheck = datetime.datetime.now()
    		
    	# if the `q` key was pressed, break from the loop
    	if key == ord("q"):
    		break
    
    # do a bit of cleanup
    cv2.destroyAllWindows() 
    
    
    return frame 

#if __name__=="__main__": 
#    main()