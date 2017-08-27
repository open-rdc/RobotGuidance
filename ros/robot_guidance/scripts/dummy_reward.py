#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('robot_guidance')
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
#from reinforcement_learning import *
from skimage.transform import resize
from std_msgs.msg import Float32, Int8

class dummy_reward:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)
        self.action_sub = rospy.Subscriber("action", Int8, self.callback_action)
        self.reward_pub = rospy.Publisher("reward", Float32, queue_size=10)
        self.action = 0
        self.reward = 0

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.img = resize(cv_image, (48, 64), mode='constant')
        cv2.imshow("Image Object", self.img)
        cv2.waitKey(1)

    def callback_action(self, data):
        return 0

#        r, g, b = cv2.split(img)
#        imgobj = np.asanyarray([r,g,b])
#        print(imgobj)
#        self.action = self.rl.act_and_trains(imgobj, self.reward)
#        print(self.action)

if __name__ == '__main__':
    dr = dummy_reward()
    rospy.init_node('dummy_reward', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
    cv2.destroyAllWindows()
