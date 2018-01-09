#!/usr/bin/env python
import rospy
from rosserial_arduino.msg import Adc


def arduino_sim():
	adc_pub = rospy.Publisher("/adc", Adc, queue_size=1)
	rospy.init_node('arduino_sim', anonymous=True)
	rate = rospy.Rate(200) # 200hz
	adc = Adc()
	adc.adc0 = 0
	adc.adc1 = 0
	adc.adc2 = 0
	adc.adc3 = 0
	adc.adc4 = 0
	adc.adc5 = 0

	while not rospy.is_shutdown():

		adc.adc0 = 100
		adc_pub.publish(adc)
		rate.sleep()

if __name__ == '__main__':
	try:
		arduino_sim()
	except rospy.ROSInterruptException:
		pass
