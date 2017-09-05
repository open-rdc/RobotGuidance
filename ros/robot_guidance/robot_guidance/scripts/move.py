#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, Int8

class robot_move:
	def __init__(self):
		rospy.init_node('robot_move', anonymous=True)
		self.action_sub = rospy.Subscriber("/action", Int8, self.callback_action)
		self.vel_pub = rospy.Publisher('/icart_mini/cmd_vel', Twist, queue_size=10)
		self.action = 0
		self.vel_msg = Twist()


	def callback_action(self, data):
		self.action = data.data

		linear_x = 0.3
		angular_z = 0.5

		if self.action == 1:
			angular_z = -angular_z
		elif self.action == 2:
			angular_z = 0
		elif self.action == 3:
			angular_z = angular_z
		else:
			linear_x = 0
			angular_z = 0

		self.vel_msg.linear.x = linear_x
		self.vel_msg.linear.y = 0
		self.vel_msg.linear.z = 0
		self.vel_msg.angular.x = 0
		self.vel_msg.angular.y = 0
		self.vel_msg.angular.z = angular_z

		if self.action == 1:
			move = 'Right'
		elif self.action == 2:
			move = 'Front'
		elif self.action == 3:
			move = 'Left'
		elif self.action == 4:
			move = 'Stop'
		elif self.action == 0:
			move = 'Stop'

		print 'action = ', move
		#Publish the velocity
		self.vel_pub.publish(self.vel_msg)

if __name__ == '__main__':
	rm = robot_move()
	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
