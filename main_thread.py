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

import my_client 
from ultrasonic import sensor 
from led import LED  
from send_email import EMAIL


def task1(ip): 
    
    my_client.client_main(ip)
    
def task2():  
    
    sonic=sensor(21,20) 
    led=LED(19) 
    email=EMAIL()
    
    while True: 
        distance=sonic.distance()   
        print (distance)
        if distance<50: 
            led.control('on')  
            email.send_email()
            time.sleep(60) 
            led.control('off')
        time.sleep(1)
            

def main(ip): 

   

    t1=threading.Thread(target=task1,args=(ip,)) 
    t2=threading.Thread(target=task2)  
    
    t1.start() 
    t2.start() 
        
    
    #t1.join() 
    #t2.join()     

if __name__=="__main__" :  
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--ip", required=True,
            help="ip address of the server to which the client will connect")

    args = vars(ap.parse_args())
    
    ip=args["ip"]
    
    main(ip)
        