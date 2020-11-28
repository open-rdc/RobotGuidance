#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('robot_guidance')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from deep_learning import *
from skimage.transform import resize
from std_msgs.msg import Float32, Int8
import sys
import skimage.transform
import csv
import os
import time
import copy

class robot_guidance_dl_node:
	def __init__(self):
		rospy.init_node('robot_guidance_dl_node', anonymous=True)
		self.action_num = rospy.get_param("/robot_guidance_node/action_num", 3)
		print("action_num: " + str(self.action_num))
		self.dl = deep_learning(n_action = self.action_num)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
		self.position_sub = rospy.Subscriber("/position", Float32, self.callback_position)
		self.action_pub = rospy.Publisher("action", Int8, queue_size=1)
		self.action = 0
		self.position = 0
		self.cv_image = np.zeros((480,640,3), np.uint8)
		self.count = 0
		self.learning = True
		self.start_time = time.strftime("%Y%m%d_%H:%M:%S")
		self.action_list = ['Front', 'Right', 'Left', 'Back', 'Stop']
		#self.path = '/home/pete/cit-1808/research_pic/'
		self.path = 'cit-1808/research_pic/'
		os.makedirs(self.path + self.start_time)

		with open(self.path + self.start_time + '/' +  'reward.csv', 'w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(['rostime', 'reward', 'action'])

	def callback(self, data):
		try:
			self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

#		cv2.imshow("Capture Image", self.cv_image)
		temp = copy.deepcopy(self.cv_image)
		cv2.circle(temp, (640 / 2, 480 / 2),  100, (0, 0, 255), 2)
		cv2.imshow("Capture Image", temp)
		cv2.waitKey(1)

	def callback_position(self, position):
		self.position = position.data
		img = resize(self.cv_image, (48, 64), mode='constant')
		r, g, b = cv2.split(img)
		imgobj = np.asanyarray([r,g,b])
		
		self.count += 1
		if self.count >= 300:
			self.learning = False
		
		ros_time = str(rospy.Time.now())
		if self.learning:
			if self.position > 10:
				self.action = 1
			elif self.position < -10:
				self.action = 2
			else:
				self.action = 0

			self.action = self.dl.act_and_trains(imgobj, self.action)

			line = [ros_time, str(self.position), str(self.action)]
			with open(self.path + self.start_time + '/' +  'reward.csv', 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(line)

		else:
			self.action = self.dl.act(imgobj)
		self.action_pub.publish(self.action)

#		cv2.putText(self.cv_image,self.action_list[self.action],(550,450), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
#		image_name = self.path + self.start_time + '/' + ros_time + '.png'
#		cv2.imwrite(image_name, self.cv_image)
		print("learning = " + str(self.learning) + " count: " + str(self.count) + " action: " + str(self.action) + ", position: " + str(round(self.position,5)))
#		if((self.count - 1) % 100 == 0 and self.count > 100):
#			self.rl.save_agent()

if __name__ == '__main__':
	rg = robot_guidance_dl_node()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
		cv2.destroyAllWindows()

