#!/usr/bin/env python
# check node
# rostopic pub -1 /adc rosserial_arduino/Adc 0 0 0 0 0 0

import rospy
from std_msgs.msg import Float32
from rosserial_arduino.msg import Adc

class guidance_reward:
	def __init__(self):
		rospy.init_node('guidance_reward', anonymous=True)
		self.poten_sub = rospy.Subscriber("/adc", Adc, self.callback_poten)
		self.reward_pub = rospy.Publisher('/reward', Float32, queue_size=10)
		self.poten = Adc()
		self.action = 0

	def callback_poten(self, data):
		self.poten = data
		self.reward_fb = 0
		self.reward_lr = 0
		self.reward = 0

		if self.poten.adc2 > 120:
			self.reward = -10000	#for testing
		else:
			self.reward_lr = 1.0 - (self.poten.adc0 + self.poten.adc1)/30.0
			self.reward_fb = 1.0 - self.poten.adc2/60.0 - self.poten.adc3/20.0
			self.reward = self.reward_fb ** 3 + self.reward_lr ** 3 - 2

		print 'LR = ', round(self.reward_lr, 4), ' \tBF = ', round(self.reward_fb, 4), '\treward = ', round(self.reward, 2)

		self.reward_pub.publish(self.reward)

if __name__ == '__main__':
	gr = guidance_reward()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
