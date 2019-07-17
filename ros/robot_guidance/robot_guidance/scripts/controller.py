#!/usr/bin/env python
# check node
# rostopic pub -1 /adc rosserial_arduino/Adc 0 0 0 0 0 0

import rospy
from std_msgs.msg import Int8
from rosserial_arduino.msg import Adc

class robot_controller:
	def __init__(self):
		rospy.init_node('robot_controller', anonymous=True)
		self.poten_sub = rospy.Subscriber("/adc", Adc, self.callback_poten)
		self.control_pub = rospy.Publisher('/control', Int8, queue_size=10)
		self.poten = Adc()
#		self.action = 0
#		self.pitch = 0
#		self.yaw = 0

	def callback_poten(self, data):
		self.poten = data
		self.control = 0
		self.correct_action = 0

		if self.poten.adc2 > 120:
			#	for testing
			self.correct_action = -1
		else:
			self.control = self.poten.adc0 - self.poten.adc1 -20
			
			if self.control > 10:
				self.correct_action = 2
			elif self.control < -10:
				self.correct_action = 1
			else:
				self.correct_action = 0

#		print 'LR = ', round(self.control, 2), '\tcontrol = ', round(self.control, 2)

		#Publish the correct_action
		self.control_pub.publish(self.correct_action)

if __name__ == '__main__':
	rc = robot_controller()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
