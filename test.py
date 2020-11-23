# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages1
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time 
# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages1
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
        '192.168.1.153'))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()


vs_class=VideoStream(usePiCamera=True)
vs = vs_class.start()


time.sleep(2.0)

start_time=time.time() 
seconds=10
while True:
        # read the frame from the camera and send it to the server
        frame = vs.read()
        sender.send_image(rpiName, frame)
        current_time=time.time() 
        elapsed_time=current_time-start_time  
        if elapsed_time > seconds: 
            print ('6seconds has passed, exiting now')  
            vs_class.stop()
            time.sleep(2) 
            print ('starting back up') 
            vs_class.start()
            
    


