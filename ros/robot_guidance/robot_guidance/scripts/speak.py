#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import os

class speak:
	def __init__(self):
		rospy.init_node('speak', anonymous=True)
		self.voice_sub = rospy.Subscriber('/voice', String, self.callback_speak)

	def callback_speak(self, data):
		self.voice = data.data
		text = 'espeak -a 200 "' + self.voice + '"'
		os.system(text)

if __name__ == '__main__':
	sp = speak()
	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting Down")
