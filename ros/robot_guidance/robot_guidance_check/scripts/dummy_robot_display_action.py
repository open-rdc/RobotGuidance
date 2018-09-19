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
import os
from os.path import expanduser
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
        self.size = 0
        self.reward = 0
        self.reward_lr = 0
        self.reward_fb = 0
        self.cv_image = np.zeros((480,640,3), np.uint8)
        self.cv_image.fill(255)
        self.image = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.arrow_cv_image = np.zeros((200,640,3), np.uint8)
        self.arrow_cv_image.fill(255)
        self.image_timer = rospy.Timer(rospy.Duration(0.1), self.callback_image_timer)
        self.reward_timer = rospy.Timer(rospy.Duration(0.1), self.callback_reward_timer)
        self.count = 0
        self.prev_count = -1
        self.display_action_mode = False
        self.display_action_x = 0
        self.display_action_y = 0
        self.display_actions = np.zeros((11,11), np.uint8)
        self.action_image = np.zeros((550,550,3), np.uint8)
        self.action_image.fill(255)
        self.action_log = [[0 for x in range(11)] for y in range(11)]
        self.action_diff_count = 0
        self.home = expanduser("~")
        self.path = self.home + '/result_pic/'
        self.start_time = time.strftime("%Y%m%d_%H:%M:%S")
        os.makedirs(self.path + self.start_time)
        self.episode_count = 0

    def callback_image_timer(self, data):
        self.cv_image.fill(255)
        cv2.circle(self.cv_image, (640 / 2 + self.pan, 480 / 2),  100 + self.size, (0, 255, 0), -1)
        self.image = self.bridge.cv2_to_imgmsg(self.cv_image, encoding="bgr8")
        self.image_pub.publish(self.image)

    def callback_action(self, data):
        if self.display_action_mode:
            self.action = data.data
            self.display_action_mode = not self.display_actions_process(False)
            if not self.display_action_mode:
                self.pan = int(np.random.rand() * 400 - 200)
                self.size = int(np.random.rand() * 50 - 50)
                print("change pan angle && circle size")
            return
        action_list = [[0, 2], [-10, 0], [10, 0], [0, 0]]
        self.action = data.data
        if (self.action < 0 or self.action >= 5):
            return
        self.pan += action_list[self.action][0]
        self.size += action_list[self.action][1]
        size_limit = 50
        pan_limit = 250
        self.size = min(max(self.size, -size_limit), size_limit)
        self.pan = min(max(self.pan, -pan_limit), pan_limit)
        self.count += 1
        if ((self.count % 100) == 0):
            self.display_action_mode = True
            self.display_actions_process(True)
#            self.pan = int(np.random.rand() * 400 - 200)
#            self.size = int(np.random.rand() * 50 - 50)
#            print("change pan angle && circle size")

#display action
        center = (320, 100)
        arrow = [(center[0], center[1]-50), (center[0]-200, center[1]), (center[0]+200, center[1]), center]
        self.arrow_cv_image.fill(255)
        cv2.line(self.arrow_cv_image, center, arrow[self.action], (0,0,200), 10)
        cv2.imshow("action", self.arrow_cv_image)
        cv2.waitKey(1)

    def callback_reward_timer(self, data):
        if self.display_action_mode:
            self.reward_pub.publish(-10000)
            return
        if (self.prev_count == self.count):
            print("reward timer is too fast!")
        self.prev_count = self.count
        self.reward_lr = min(1.0 - abs(self.pan) / 100.0, 1.0)
        self.reward_fb = min(1.0 - abs(self.size) / 25.0, 1.0)
        self.reward_lr = self.reward_lr ** 3 - 0.5
        self.reward_fb = self.reward_fb ** 3 - 0.5
        self.reward = self.reward_lr + self.reward_fb
#        print("selected_action: " + str(self.action) + ", reward: " + str(self.reward))
        self.reward_pub.publish(self.reward)

    def display_actions_process(self, init_flag):
        if init_flag:
            self.display_action_x = 0
            self.display_action_y = 0
            self.action_image.fill(255)
            self.action_diff_count = 0
            self.episode_count += 1
        else:
            self.display_actions[self.display_action_x][self.display_action_y] = self.action
            center = (50 * self.display_action_x + 25, 50 * self.display_action_y + 25)
            arrow = [(center[0], center[1]+25), (center[0]-25, center[1]), (center[0]+25, center[1]), center]
            if self.action_log[self.display_action_x][self.display_action_y] == self.display_actions[self.display_action_x][self.display_action_y]:
                color = 0
            else:
                color = 255
                self.action_diff_count += 1
            cv2.circle(self.action_image, center, 5, (0, 0, color))
            cv2.line(self.action_image, center, arrow[self.action], (0, 0, color), 2)
            self.action_log[self.display_action_x][self.display_action_y] = self.display_actions[self.display_action_x][self.display_action_y]

            if self.display_action_x == 10 and self.display_action_y == 10:
                cv2.putText(self.action_image, str(self.action_diff_count), (510,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
                image_name = self.path + self.start_time + '/episode' + str(self.episode_count) + '.png'
                cv2.imwrite(image_name, self.action_image)
            cv2.imshow("actions", self.action_image)
            cv2.waitKey(1)

            self.display_action_x += 1
            if self.display_action_x > 10:
                self.display_action_x = 0
                self.display_action_y += 1
                if self.display_action_y > 10:
                    return True

        self.pan = self.display_action_x * 50 - 250
        self.size = self.display_action_y * 10 - 50
        return False

if __name__ == '__main__':
    dr = dummy_robot()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
cv2.destroyAllWindows()
