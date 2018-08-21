#!/usr/bin/env python
# check node
# rostopic pub -1 /action std_msgs/Int8 1

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, Int8

linear_vel = 0.05
angle_vel = 0.1

class robot_move:
	def __init__(self):
		rospy.init_node('robot_move', anonymous=True)
		self.action_sub = rospy.Subscriber("/action", Int8, self.callback_action)
		self.vel_pub = rospy.Publisher('/icart_mini/cmd_vel', Twist, queue_size=1)
		self.action = 0
		self.vel_msg = Twist()

	def callback_action(self, data):
		self.action = data.data

		velocity = [[linear_vel, 0.0],  [0.0, -angle_vel], [0.0, angle_vel],[0.0, 0,0], [-linear_vel, 0.0]]

		self.vel_msg.linear.x = velocity[self.action][0]
		self.vel_msg.angular.z = velocity[self.action][1]
		print 'velocity = ', self.vel_msg

		move = ['Front', 'Right', 'Left', 'Stop', 'Back']
		print 'action = ', move[self.action]

		self.vel_pub.publish(self.vel_msg)

if __name__ == '__main__':
	rm = robot_move()
	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
