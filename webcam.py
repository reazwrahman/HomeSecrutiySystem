#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:11:27 2020

@author: Reaz
"""

import cv2  

window_name="Live Video Feed"
cv2.namedWindow(window_name)
camera=cv2.VideoCapture(1) # create an object  
print ('go1')

#camera.set(3,400) 
#camera.set(4,300) 
#print (f'width= {camera.get(3)}')
 
if camera.isOpened(): # try to get the first frame
    rval, frame = camera.read()   
    print (rval)
    #bw_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    
else:
    rval = False  
    print (rval)

while rval:
    cv2.imshow(window_name, frame) 
    #cv2.imshow("Gray",bw_frame)
    rval, frame = camera.read()  
    #bw_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #print (f'rval= {rval}') 
    #print (f'frame= {frame}')
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
camera.release()
cv2.destroyWindow(window_name)
