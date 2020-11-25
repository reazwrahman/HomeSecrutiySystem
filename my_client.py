
# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages1
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time 

 


def client_main(server_ip,interrupt): 
    
 
    sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
            server_ip))    
   
    rpiName = socket.gethostname() 
    
    vs = VideoStream(usePiCamera=True).start()
      
    time.sleep(2.0)
    
    while True:  
        #print ('STATE OF INTERRUPT ='+str(interrupt)) 
        
        if interrupt==0: 
            frame = vs.read()
            sender.send_image(rpiName, frame)  
        
        elif interrupt==1:   
            print ('INTERRUPT HAS BEEN SET TO 1')
            #vs.stop()
             

if __name__=="__main__": 
    client_main('192.168.1.153',0)