#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('robot_guidance')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from reinforcement_learning import *
from skimage.transform import resize
from std_msgs.msg import Float32, Int8
from rosserial_arduino.msg import Adc
import sys
import skimage.transform
import time

class robot_guidance_node:
    def __init__(self):
        rospy.init_node('robot_guidance_node', anonymous=True)
        self.rl = reinforcement_learning(3)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
#        self.reward_sub = rospy.Subscriber("/reward", Float32, self.callback_reward)
        self.action_pub = rospy.Publisher("action", Int8, queue_size=10)
        self.poten_sub = rospy.Subscriber("/adc", Adc, self.callback_poten)
        self.action = 0
        self.reward = 0
        self.poten = Adc()

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        img = resize(cv_image, (48, 64), mode='constant')
        cv2.imshow("Capture Image", cv_image)
        #cv2.imshow("Image Object", img)
        cv2.waitKey(1)

        r, g, b = cv2.split(img)
        imgobj = np.asanyarray([r,g,b])
#        print(imgobj)
        self.reward = 2.0 - (self.poten.adc0 + self.poten.adc1 + self.poten.adc2*2 + self.poten.adc3*2)/100.0
        self.action = self.rl.act_and_trains(imgobj, self.reward)
        self.action_pub.publish(self.action)

        print("action: " +str(self.action) + ", reward: " + str(self.reward))
        time.sleep(1)

    def callback_poten(self, data):
        self.poten = data
        return 0

#    def callback_reward(self, reward):
#        self.reward = reward.data
#        return 0

if __name__ == '__main__':
    rg = robot_guidance_node()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
