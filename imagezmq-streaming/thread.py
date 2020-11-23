#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 02:49:25 2020

@author: Reaz
"""

import threading  
from my_client import CLIENT  
import time

global a
a=CLIENT() 

def run(): 
    global a  
    print ('thread 1 running')
    a.run(0)  
    print ('thread 1 running still')
    
def stop(): 

    global a
        
    print (a.frame)  
    time.sleep(2)
    a.stop() 
    print ('vs stopped') 
    time.sleep(5) 
    print ('starting back up')  
    a.start() 
    a.run(0)
        
    
t1=threading.Thread(target=run) 
t2=threading.Thread(target=stop)   

t1.start() 
t2.start()