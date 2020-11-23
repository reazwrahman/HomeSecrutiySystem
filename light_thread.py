#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 03:57:51 2020

@author: Reaz
"""

import threading
import os 
import time  
import argparse  
import RPi.GPIO as GPIO 
from imutils.video import VideoStream

from my_client import CLIENT
from ultrasonic import sensor 
from led import LED  
from send_email import EMAIL 
from camera import CAMERA 


####### FOR INTERRUPT SUBROUTINE #######
global interrupt  
interrupt=0  
###################################


def task1():    
    
    def subroutine(): 
        time.sleep(2) 
        picam=CAMERA() 
        picam.take_multiple_pics()  
        email=EMAIL() 
        email.send_email_with_images(picam.filenames)
        
        
    global interrupt 
    a=CLIENT()  
    a.start() 
    
    
        
    while True: 
        if interrupt==0:  
            a.run() 
        if interrupt==1:   
            print ('--------------')
            print ('INTERRUPT='+str(interrupt)) 
            print ('--------------')
            a.stop() 
            subroutine()  
            interrupt=1
            a=CLIENT()   
            interrupt=0 
            try: 
                a.start()  
                a.run()
            except ValueError: 
                a.run()
        
        
#            try: 
#                a.start() 
#                a.run() 
#            except: 
#                a.run() 
#            finally: 
#                pass
#            
 
    
def task2(status='off'):  
    
    global interrupt
    
    sonic=sensor(21,20) 
    led=LED(19) 
    led.control(status) 
    
    
    while True:  
        try:
            distance=sonic.distance()   
            print (distance)
            if distance<50:  
                led.control('on')   
                interrupt=1   
                time.sleep(60) 
                led.control(status) 
            time.sleep(1)
         
        except: 
             print ('encountered hardware issue, thread 2 failed')
       
        
                                                    
def main(ip,light): 


    global interrupt
   
    t1=threading.Thread(target=task1) 
    t2=threading.Thread(target=task2,args=(light,))  
    
    
    t1.start() 
    t2.start() 

    
    
    #t1.join() 
    #t2.join()     

if __name__=="__main__" :  
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--ip", required=True,
            help="ip address of the server to which the client will connect")

    ap.add_argument("-l", "--light", required=True,
            help="whether to keep the light on or off")
    args = vars(ap.parse_args())
    
    ip=args["ip"] 
    status=args["light"]
    
    
    main(ip,status) 
    
        