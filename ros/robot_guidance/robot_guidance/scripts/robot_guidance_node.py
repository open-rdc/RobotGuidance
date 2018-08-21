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
from std_msgs.msg import Float32, Int8, String
import sys
import skimage.transform
import csv
import os
import time
import numpy as np

class robot_guidance_node:
	def __init__(self):
		rospy.init_node('robot_guidance_node', anonymous=True)
		self.action_num = rospy.get_param("/robot_guidance_node/action_num", 4)
		print("action_num: " + str(self.action_num))
		self.rl = reinforcement_learning(n_action = self.action_num)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
		self.reward_sub = rospy.Subscriber("/reward", Float32, self.callback_reward)
		self.action_pub = rospy.Publisher("action", Int8, queue_size=1)
		self.voice_pub = rospy.Publisher("voice", String, queue_size=1)
		self.action = 0
		self.reward = 0
		self.cv_image = np.zeros((480,640,3), np.uint8)
		self.count = 0
		self.learning = True
		self.start_time = time.strftime("%Y%m%d_%H:%M:%S")
		self.action_list = ['Forward', 'Right', 'Lleft', 'Stop', 'Back']
		self.path = '/home/pete/cit-1808/research_pic/'
		os.makedirs(self.path + self.start_time)
		self.learning_flag = True
		self.count_flag = False
		self.skip_start = 0
		self.all_log = 0
		self.save_log = 0
		self.log_count = 0
		os.system('espeak -a 200 Ready')

		with open(self.path + self.start_time + '/' +  'reward.csv', 'w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(['ros_time', 'reward', 'action'])

		with open(self.path + self.start_time + '/' +  'action_log.csv', 'w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(['ros_time', 'action'])

		with open(self.path + self.start_time + '/' +  'moving_action_log.csv', 'w') as f:
			writer = csv.writer(f, lineterminator='\n')
			writer.writerow(['ros_time', 'action'])

#		self.callback()

	#opencv
#	def callback(self):
#		self.cap = cv2.VideoCapture(1)
#		while True:
#			ret, self.cv_image = self.cap.read()
#			cv2.imshow("Capture Image", self.cv_image)
#			if cv2.waitKey(1) & 0xFF == ord('q'):
#				break

	def callback(self, data):
		try:
			self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		cv2.imshow("Capture Image", self.cv_image)
		cv2.waitKey(1)

	def callback_reward(self, reward):
		ros_time = str(rospy.Time.now())

		self.reward = reward.data
		img = resize(self.cv_image, (48, 64), mode='constant')
		r, g, b = cv2.split(img)
		imgobj = np.asanyarray([r,g,b])

		if self.reward == -10000: #	for testing
			self.learning = False
		else:
			self.learning = True

		#act and save reward log
		if self.learning:
			if not self.learning_flag:
				self.learning_flag = True
			self.action = self.rl.act_and_trains(imgobj, self.reward)
			line = [ros_time, str(self.reward), str(self.action)]
			with open(self.path + self.start_time + '/' +  'reward.csv', 'a') as f:
				writer = csv.writer(f, lineterminator='\n')
				writer.writerow(line)
			self.count += 1
			if self.count % 2000 == 0:
				self.count_flag = True

		#test_experiment
		else:
			if self.learning_flag and self.count_flag:
				self.learning_flag = False
				self.count_flag = False
				self.save_log = 0
				self.skip_start = 0
				self.all_log = 0
			self.action = self.rl.act(imgobj)

			if self.skip_start >= 50 and self.all_log < 20:
				if self.save_log == 5:
					self.voice_pub.publish(self.action_list[self.action])
				if self.save_log < 10:
					line = [ros_time, str(self.action)]
					with open(self.path + self.start_time + '/' +  'moving_action_log.csv', 'a') as f:
						writer = csv.writer(f, lineterminator='\n')
						writer.writerow(line)
				else:
					if self.save_log == 10:
						self.voice_pub.publish('recording')

					if self.save_log == 15:
						self.voice_pub.publish(self.action_list[self.action])

					line = [ros_time, str(self.action)]
					with open(self.path + self.start_time + '/' +  'action_log.csv', 'a') as f:
						writer = csv.writer(f, lineterminator='\n')
						writer.writerow(line)

					if self.save_log == 19:
						self.all_log += 1
						self.save_log = -1
						print('testing : ' + str(self.all_log))
						if self.all_log % 20 == 0:
							self.voice_pub.publish('end Testing')
							line = 'end test'
							with open(self.path + self.start_time + '/' +  'action_log.csv', 'a') as f:
								writer = csv.writer(f, lineterminator='\n')
								writer.writerow(line)
						elif self.all_log % 5 == 0:
							self.voice_pub.publish('change row')
							line = 'change row'
							with open(self.path + self.start_time + '/' +  'action_log.csv', 'a') as f:
								writer = csv.writer(f, lineterminator='\n')
								writer.writerow(line)
						else:
							self.voice_pub.publish('Move')
							with open(self.path + self.start_time + '/' +  'action_log.csv', 'a') as f:
								writer = csv.writer(f, lineterminator='\n')
								writer.writerow(str(self.all_log))
						line = ''
						with open(self.path + self.start_time + '/' +  'action_log.csv', 'a') as f:
							writer = csv.writer(f, lineterminator='\n')
							writer.writerow(line)
						with open(self.path + self.start_time + '/' +  'moving_action_log.csv', 'a') as f:
							writer = csv.writer(f, lineterminator='\n')
							writer.writerow(line)

					self.log_count += 1
				self.save_log += 1
			else:
				self.skip_start += 1
		self.action_pub.publish(self.action)

		#write action on image and save image
		cv2.putText(self.cv_image,self.action_list[self.action],(550,450), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)
		image_name = self.path + self.start_time + '/' + ros_time + '.png'
		cv2.imwrite(image_name, self.cv_image)

		print("count: " + str(self.count) + ", learning = " + str(self.learning) + ", action: " + str(self.action) + ", reward: " + str(round(self.reward,5)))

#		if((self.count-1) % 100 == 0 and self.count > 500):
#			self.rl.save_agent()

		if self.learning:
			if self.count % 2000 == 0:
				self.voice_pub.publish('Start Testing')
			elif self.count % 50 == 0:
				self.voice_pub.publish(str(self.count))
			elif self.count % 5 == 0:
				self.voice_pub.publish(self.action_list[self.action])

if __name__ == '__main__':
	rg = robot_guidance_node()
	try:
		rospy.spin()
	except:
		print("Shutting Down")
		cap.release()
		cv2.destroyAllWindows()
