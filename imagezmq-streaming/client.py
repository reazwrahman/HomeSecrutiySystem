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

# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-s", "--server-ip", required=True,
#        help="ip address of the server to which the client will connect")
#
#ap.add_argument("-c", "--camera", required=True,
#                help="define which camera to use picam or usbcam")
#args = vars(ap.parse_args())
#
#camera=args['camera']

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
        '192.168.1.153'))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()



vs = VideoStream(usePiCamera=True).start()


time.sleep(2.0)

while True:
        # read the frame from the camera and send it to the server
        frame = vs.read()
        sender.send_image(rpiName, frame)



#
#start_time=time.time() 
#seconds=10
#while True:
#	# read the frame from the camera and send it to the server
#	frame = vs.read()
#	sender.send_image(rpiName, frame)  
#	current_time=time.time() 
##	elapsed_time=current_time-start_time  
##	if elapsed_time > seconds: 
##		print ('6seconds has passed, exiting now') 
##		break 
#		
##time.sleep(2) 
##print ('taking pi pic now')  
##a.take_multiple_pics()
#
#    
