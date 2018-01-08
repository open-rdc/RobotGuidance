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
import sys
import skimage.transform
import csv
import os
import time

class robot_guidance_node:
	def __init__(self):
		rospy.init_node('robot_guidance_node', anonymous=True)
		self.action_num = rospy.get_param("/robot_guidance_node/action_num", 3)
		print("action_num: " + str(self.action_num))
		self.rl = reinforcement_learning(n_action = self.action_num)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
		self.reward_sub = rospy.Subscriber("/reward", Float32, self.callback_reward)
		self.action_pub = rospy.Publisher("action", Int8, queue_size=1)
		self.action = 0
		self.reward = 0
		self.cv_image = np.zeros((480,640,3), np.uint8)
		self.count = 0
		self.learning = True
		self.action_list = ['Front', 'Right', 'Left', 'Back', 'Stop']

	def callback(self, data):
		try:
			self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		cv2.imshow("Capture Image", self.cv_image)
		cv2.waitKey(1)

	def callback_reward(self, reward):
		self.reward = reward.data
		img = resize(self.cv_image, (48, 64), mode='constant')
		r, g, b = cv2.split(img)
		imgobj = np.asanyarray([r,g,b])

		if self.reward == -10000: #	for testing
			self.learning = False
		else:
			self.learning = True

		ros_time = str(rospy.Time.now())
		if self.learning:
			self.action = self.rl.act_and_trains(imgobj, self.reward)
			self.count += 1
		else:
			self.action = self.rl.act(imgobj)
		self.action_pub.publish(self.action)

		print("learning = " + str(self.learning) + " count: " + str(self.count) + " action: " + str(self.action) + ", reward: " + str(round(self.reward,5)))

if __name__ == '__main__':
	rg = robot_guidance_node()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
		cv2.destroyAllWindows()
