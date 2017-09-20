#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('robot_guidance')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32, Int8
import numpy as np
import time

class dummy_robot:
    def __init__(self):
        rospy.init_node('dummy_robot', anonymous=True)
        self.bridge = CvBridge()
        self.image_pub = rospy.Publisher("image_raw", Image, queue_size=1)
        self.reward_pub = rospy.Publisher("reward", Float32, queue_size=1)
        self.action_sub = rospy.Subscriber("action", Int8, self.callback_action)
        self.action = 0
        self.pan = 0
        self.reward = 0
        self.cv_image = np.zeros((480,640,3), np.uint8)
        self.cv_image.fill(255)
        self.image = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.timer = rospy.Timer(rospy.Duration(0.033), self.callback_timer)
        self.count = 0
        self.s = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.num = 0

    def callback_timer(self, data):
#        print('Timer called at ' + str(data.current_real))
        self.cv_image.fill(255)
        self.count += 1
        if ((self.count % 100) == 0):
            self.pan = int(np.random.rand() * 400 - 200)
            print("change pan angle")
            self.s = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            self.num = 0
        cv2.circle(self.cv_image, (640 / 2 + self.pan, 480 / 2), 200, (0, 255, 0), -1)
        self.image = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.image_pub.publish(self.image)

    def callback_action(self, data):
#        action_list = [0, -10, 10]
        action_list = [[0, 0, 0], [-2, -4, -2], [2, 4, 2]]
        self.action = data.data
        if (self.action < 0 or self.action >= 3):
            return
#        self.pan += action_list[self.action]
        self.num = (self.num % 3)
        self.s[self.num] = action_list[self.action]
        move = self.s[0][self.num] + self.s[1][(self.num + 2) % 3] + self.s[2][(self.num + 1) % 3]
        if move > 4:
            move = 4
        elif move < -4:
            move = -4

#        print("s = " + str(self.s))
#        print("num = " + str(self.num) + " move = " + str(move))
#        time.sleep(1)
        self.num += 1
        self.pan += move
        self.reward = 1.0 - abs(self.pan) / 100.0

#        print("selected_action: " + str(self.action) + ", reward: " + str(self.reward))
        self.reward_pub.publish(self.reward)

if __name__ == '__main__':
    dr = dummy_robot()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
