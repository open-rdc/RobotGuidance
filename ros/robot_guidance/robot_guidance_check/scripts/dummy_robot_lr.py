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
        self.arrow_cv_image = np.zeros((100,640,3), np.uint8)
        self.arrow_cv_image.fill(255)
        self.image_timer = rospy.Timer(rospy.Duration(0.033), self.callback_image_timer)
        self.reward_timer = rospy.Timer(rospy.Duration(0.2), self.callback_reward_timer)
        self.count = 0
        self.prev_count = -1

    def callback_image_timer(self, data):
        self.cv_image.fill(255)
        cv2.circle(self.cv_image, (640 / 2 + self.pan, 480 / 2), 200, (0, 255, 0), -1)
        self.image = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.image_pub.publish(self.image)

    def callback_action(self, data):
        action_list = [0, -10, 10]
        self.action = data.data
        if (self.action < 0 or self.action >= 3):
            return
        self.pan += action_list[self.action]
        self.count += 1
        if ((self.count % 200) == 0):
            self.pan = int(np.random.rand() * 400 - 200)
            print("change pan angle")

        pt1 = (320, 50)
        if (self.action == 1):
            pt2 = (320 - 200, 50)
        elif (self.action == 2):
            pt2 = (320 + 200, 50)
        elif (self.action == 3):
            pt2 = (320, 50 + 50)
        else:
            pt2 = (320, 50)
        self.arrow_cv_image.fill(255)
        cv2.line(self.arrow_cv_image, pt1, pt2, (0, 0, 200), 10)
        cv2.imshow("action", self.arrow_cv_image)
        cv2.waitKey(1)

    def callback_reward_timer(self, data):
        if (self.prev_count == self.count):
            print("reward timer is too first!")
        self.prev_count = self.count
        self.reward = min(1.0 - abs(self.pan) / 100.0, 1.0)
        self.reward = self.reward ** 3
#        print("selected_action: " + str(self.action) + ", reward: " + str(self.reward))
        self.reward_pub.publish(self.reward)

if __name__ == '__main__':
    dr = dummy_robot()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
cv2.destroyAllWindows()
