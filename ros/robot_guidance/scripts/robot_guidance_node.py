#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import reinforcement_learning as RL
import cv_bridge
import skimage.transform

def callback(imgmsg):
    bridge = cv_bridge

def robot_guidance_node():
    rl = RL()
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', String, callback)

if __name__ == '__main__':
    rospy.init_node('robot_guidance_node')
    app = robot_guidance_node()
    rospy.spin()

