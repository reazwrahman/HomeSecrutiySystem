
# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages1
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time 

 
class CLIENT(object): 
    
    def __init__(self,ip='192.168.1.153'): 
         
        self.ip=ip
        #self.vs= VideoStream(src=0) 
        self.vs=VideoStream(usePiCamera=True) 
        self.sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
                self.ip))  

        self.rpiName= socket.gethostname() 
        self.frame=None

    def run(self): 

        self.frame = self.vs.read()
        self.sender.send_image(self.rpiName, self.frame)   
            

    def stop(self): 
    
        self.vs.stop()   

    def start(self): 
        
        self.vs.start() 
        time.sleep(2.0)
        self.vs.start()             
    

if __name__=="__main__":  
    a=CLIENT() 
    a.start()
    while True: 
        a.run()
    