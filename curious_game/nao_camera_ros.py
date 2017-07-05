from __future__ import print_function
#!/usr/bin/env python
# import roslib
# roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
# from sensor_msgs.msg import Image
from sensor_msgs import msg
from cv_bridge import CvBridge, CvBridgeError
from naoqi import ALProxy
import time
import Image
import numpy as np


class image_converter:

    def __init__(self):
        self.robotIP = '192.168.0.104'
        self.port = 9559

        self.image_pub = rospy.Publisher("/cam0//usb_cam/image_raw", msg.Image)

        self.bridge = CvBridge()
        self.camProxy = ALProxy("ALVideoDevice", self.robotIP, self.port)
        self.resolution = 2  # VGA
        self.colorSpace = 11  # RGB


    def start(self):
        # init a listener to kinect and
        rospy.init_node('image_converter')
        self.videoClient = self.camProxy.subscribe("python_client", self.resolution, self.colorSpace, 5)

        t0 = time.time()

        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        while True:
            naoImage = self.camProxy.getImageRemote(self.videoClient)
            if naoImage is not None:
                imageWidth = naoImage[0]
                imageHeight = naoImage[1]
                array = naoImage[6]

                # Create a PIL Image from our pixel array.
                im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(np.array(im), "bgr8"))
            else:
                print('did not get camera')
                break

        # rospy.spin()
        self.camProxy.unsubscribe(self.videoClient)


ic = image_converter()
ic.start()