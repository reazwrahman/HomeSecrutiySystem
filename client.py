# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages1
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
        help="ip address of the server to which the client will connect")

ap.add_argument("-c", "--camera", required=True,
                help="define which camera to use picam or usbcam")
args = vars(ap.parse_args())

camera=args['camera']

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
        args["server_ip"]))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname() 

if camera=="picam":
        vs = VideoStream(usePiCamera=True).start()
if camera=="usbcam":
        vs = VideoStream(src=0).start()

time.sleep(2.0)

while True:
        # read the frame from the camera and send it to the server
        frame = vs.read()
        sender.send_image(rpiName, frame)