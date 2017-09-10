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
		self.action = 0
		self.poten = Adc()

	def callback_poten(self, data):
		self.poten = data
		self.reward = 2.0 - (self.poten.adc0 + self.poten.adc1 + self.poten.adc2 * 2 + self.poten.adc3 * 2) / 100.0

		print 'reward = ', self.reward

		#Publish the velocity
		self.reward_pub.publish(self.reward)

if __name__ == '__main__':
	gr = guidance_reward()
	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
