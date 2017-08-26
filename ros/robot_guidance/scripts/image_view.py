#!/usr/bin/env python
from __future__ import print_function
import roslib
roslib.load_manifest('robot_guidance')
import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_view:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv2.imshow("Image windows", cv_image)
        cv2.waitKey(3)

if __name__ == '__main__':
    im = image_view()
    rospy.init_node('image_view', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

