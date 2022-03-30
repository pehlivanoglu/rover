#!/usr/bin/env python

from moviepy.editor import VideoFileClip

from cv_bridge import CvBridge

from sensor_msgs.msg import Image

import cv2 
import numpy as np 
import rospy

from geometry_msgs.msg import Twist

import time

desired_aruco_dictionary = "DICT_APRILTAG_36h11"

ARUCO_DICT = {
  "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
  "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
  "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
  "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
  "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
  "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
  "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
  "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
  "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
  "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
  "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
  "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
  "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
  "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
  "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
  "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
  "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(args["type"]))
	sys.exit(0)
	
print("[INFO] detecting '{}' markers...".format(desired_aruco_dictionary))


def callback(data):
	bridge = CvBridge()
	cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
	(rows,cols,channels) = cv_image.shape

	this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
	this_aruco_parameters = cv2.aruco.DetectorParameters_create()

	frames = cv_image
	frames = cv2.resize(frames, (640, 480), interpolation=cv2.INTER_AREA)
	marker_dict = {}
	positions = []

	

	(corners, ids, rejected) = cv2.aruco.detectMarkers(frames, this_aruco_dictionary, parameters=this_aruco_parameters)
	print(len(corners))
	if len(corners) > 0:
		
		print(2)	
		ids = ids.flatten()
		for(marker_corner, marker_id) in zip(corners, ids):
   
		# Extract the marker corners
			corners = marker_corner.reshape((4, 2))
			(top_left, top_right, bottom_right, bottom_left) = corners
		 
		# Convert the (x,y) coordinate pairs to integers
			top_right = (int(top_right[0]), int(top_right[1]))
			bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
			bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
			top_left = (int(top_left[0]), int(top_left[1]))
		 
		# Draw the bounding box of the ArUco detection
			cv2.line(frames, top_left, top_right, (0, 255, 0), 2)
			cv2.line(frames, top_right, bottom_right, (0, 255, 0), 2)
			cv2.line(frames, bottom_right, bottom_left, (0, 255, 0), 2)
			cv2.line(frames, bottom_left, top_left, (0, 255, 0), 2)
		 
		# Calculate and draw the center of the ArUco marker
			center_x = int((top_left[0] + bottom_right[0]) / 2.0)
			center_y = int((top_left[1] + bottom_right[1]) / 2.0)
			cv2.circle(frames, (center_x, center_y), 4, (0, 0, 255), -1)
		 
		# Draw the ArUco marker ID on the video frame
		# The ID is always located at the top_left of the ArUco marker
			cv2.putText(frames, str(marker_id),(top_left[0], top_left[1] - 15),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)

			dist_sq = (320-center_x)**2 + (480-center_y)**2
			positions.append([(320-center_x), (480-center_y)])
			start_point = (320, 480)
			end_point = (center_x, center_y)
			cv2.putText(frames, str(dist_sq), (top_left[0]- 50, top_left[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.line(frames, start_point, end_point, (255, 0, 0), 5)
			marker_dict[f"{marker_id}"] = dist_sq

	cv2.imshow('RealSense',frames)
	if cv2.waitKey(1) == ord('q'):
		exit()

def listener():
	rospy.init_node('ar_tag_detection', anonymous=True)
	rospy.Subscriber("camera/image_raw", Image, callback)
	rospy.spin()

if __name__ == "__main__":
	while not rospy.is_shutdown():
		listener()

	cv2.destroyAllWindows()	