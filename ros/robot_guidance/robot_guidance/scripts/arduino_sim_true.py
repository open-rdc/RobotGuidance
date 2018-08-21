#!/usr/bin/env python
import rospy
from rosserial_arduino.msg import Adc
import time
from random import randint
import keyboard


def arduino_sim():
	adc_pub = rospy.Publisher("/adc", Adc, queue_size=1)
	rospy.init_node('arduino_sim', anonymous=True)
	adc = Adc()
	adc.adc0 = 0
	adc.adc1 = 0
	adc.adc2 = 0
	adc.adc3 = 0
	adc.adc4 = 0
	adc.adc5 = 0
	training = True

	while not rospy.is_shutdown():

		adc.adc0 = 0
		adc.adc1 = 0
		adc.adc2 = 0
		adc.adc3 = 0

		if randint(0,1) == 0:
			adc.adc0 = randint(0, 60)
		else:
			adc.adc1 = randint(0, 60)
		if randint(2,3) == 2:
			adc.adc2 = randint(0, 60)
		else:
			adc.adc3 = randint(0, 30)

		adc_pub.publish(adc)
		time.sleep(0.6)

if __name__ == '__main__':
	try:
		arduino_sim()
	except rospy.ROSInterruptException:
		pass
