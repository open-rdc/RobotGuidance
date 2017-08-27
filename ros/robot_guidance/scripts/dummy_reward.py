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

class dummy_reward:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
        self.action_sub = rospy.Subscriber("/action", Int8, self.callback_action)
        self.reward_pub = rospy.Publisher("reward", Float32, queue_size=10)
        self.action = 0
        self.desired_action = 0
        self.reward = 0

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

#        self.img = resize(cv_image, (48, 64), mode='constant')
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV_FULL)
        h = hsv[:,:, 0]
        s = hsv[:,:, 1]
        v = hsv[:,:, 2]
        mask = np.zeros(h.shape, dtype=np.uint8)
        mask[((h < 20) | (h > 200)) & (s > 128) & (v > 128)] = 255
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            if ((rect[2] > 100) & (rect[3] > 100)):
                rects.append(np.array(rect))
        for rect in rects:
            cv2.rectangle(cv_image, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
        cv2.imshow("Image Object", cv_image)
        cv2.waitKey(1)
        if not rects:
            self.desired_action = 0
        else:
            rect = rects[0]
            if rect[3] > 300:
                self.desired_action = 4
            else:
                x = rect[0] + rect[2] / 2
                if x < 200:
                    self.desired_action = 1
                elif x > (640-200):
                    self.desired_action = 3
                else:
                    self.desired_action = 2
#        print("desired_action: " + str(self.desired_action))

    def callback_action(self, data):
        self.action = data.data
        if self.action == self.desired_action:
            self.reward = 1
        else:
            self.reward = -1
        print("selected_action: " + str(self.action) + ", desired_action: " + str(self.desired_action) + ", reward: " + str(self.reward))
        self.reward_pub.publish(self.reward)

if __name__ == '__main__':
    dr = dummy_reward()
    rospy.init_node('dummy_reward', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
