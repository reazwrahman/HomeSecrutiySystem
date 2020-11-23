#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:18:32 2020

@author: Reaz
"""

import argparse 

ap = argparse.ArgumentParser() 
ap.add_argument("-c", "--camera", required=True,  
                help="define which camera to use picam or usbcam") 
args = vars(ap.parse_args())
camera=args['camera'] 

if camera=="picam": 
    print ("pi camera") 
elif camera=="usbcam": 
    print("usbcam")
