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
from std_msgs.msg import Int8
import sys
import skimage.transform
import csv
import os
import time
import copy

class machine_learning_node:
	def __init__(self):
		rospy.init_node('machine_learning_node', anonymous=True)
		self.action_num = rospy.get_param("/machine_learning__node/action_num", 3)
		print("action_num: " + str(self.action_num))
		self.dl = deep_learning(n_action = self.action_num)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
		self.control_sub = rospy.Subscriber("/control", Int8, self.callback_learning)
                self.action_pub = rospy.Publisher("action", Int8, queue_size=1)
		self.action = 0
		self.correct_action = 0
                self.correct = 0
                self.correct_ratio = 0
                self.cv_image = np.zeros((480,640,3), np.uint8)
		self.count = 0
		self.learning = True
		self.start_time = time.strftime("%Y%m%d_%H:%M:%S")
		self.action_list = ['Front', 'Right', 'Left', 'Back', 'Stop']
		#self.path = '/home/pete/cit-1808/research_pic/'
		self.path = 'cit-1808/research_pic/'
		os.makedirs(self.path + self.start_time)

		with open(self.path + self.start_time + '/' +  'action.csv', 'w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(['rostime', 'control', 'action'])
		self.done = False

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

	def callback_learning(self, controller):
		self.correct_action = controller.data
		img = resize(self.cv_image, (48, 64), mode='constant')
		r, g, b = cv2.split(img)
		imgobj = np.asanyarray([r,g,b])

		if self.correct_action == -1: #	for testing
			self.learning = False
		else:
			self.learning = True


		ros_time = str(rospy.Time.now())
		if self.learning:
			self.count += 1
			self.action = self.dl.act_and_trains(imgobj, self.correct_action)

			line = [ros_time, str(self.correct_action), str(self.action)]
			with open(self.path + self.start_time + '/' +  'action.csv', 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(line)

#		else:
#			self.action = self.rl.act(imgobj)
		self.action_pub.publish(self.correct_action)

#		cv2.putText(self.cv_image,self.action_list[self.action],(550,450), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
#		image_name = self.path + self.start_time + '/' + ros_time + '.png'
#		cv2.imwrite(image_name, self.cv_image)
#                print(imgobj)
#		self.correct_ratio = 0.97 * self.correct_ratio + 0.03 * self.correct
		print("learning = " + str(self.learning) + " count: " + str(self.count) + " correct_action: " + str(self.correct_action) + " action: " + str(self.action))
#		if((self.count - 1) % 100 == 0 and self.count > 100):
#			self.rl.save_agent()


if __name__ == '__main__':
	ml = machine_learning_node()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
		cv2.destroyAllWindows()
