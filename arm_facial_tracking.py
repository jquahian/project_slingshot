import odrive
import time
import numpy as np
import cv2
import math
from odrive.enums import *

#soft minimums
ax0_min_lim = 0
ax1_min_lim = 0

# soft maximums
ax0_max_lim = 262144 # 180 degrees of rotation
ax1_max_lim = 393216 # 135 degrees of rotation

# centered position
ax0_centered = 131072
ax1_centered = 189326

# gear ratios for the axis
ax0_gearing = 64
ax1_gearing = 128

# encoder counts per revolution
encoder_cpr = 8192

font = cv2.FONT_HERSHEY_PLAIN
font_size = 1
main_font_color = (255, 255, 255)
red_font_color = (0, 0, 255)
blue_font_color = (255, 0, 0)
green_font_color = (0, 255, 0)
search_radius = 15

print('\n\nbeginning calibration...')
# find the first odrive
drive_1 = odrive.find_any()

# calibrate the motors
drive_1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("\nnow calibrating axis 0")
while drive_1.axis0.current_state != AXIS_STATE_IDLE:
	time.sleep(3.0)

drive_1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("now calibrating axis 1")
while drive_1.axis1.current_state != AXIS_STATE_IDLE:
	time.sleep(3.0)

# enter closed-loop control for both motors
print("\nentering closed-loop control")
drive_1.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
drive_1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# move off of home to home position which is rougly centered
print("\nmoving to home")
drive_1.axis0.controller.pos_setpoint = ax0_centered
drive_1.axis1.controller.pos_setpoint = ax1_centered
print("axis 0 homed at: {} \naxis 1 homed at: {}".format(ax0_centered, ax1_centered))
time.sleep(3.0)

# specify correct path when changing computers
frontalface_path = 'C:/Users/APIL/Anaconda3/envs/tf_1_8/Library/etc/haarcascades/haarcascade_frontalface_default.xml'

face_cascade = cv2.CascadeClassifier(frontalface_path)

video_capture = cv2.VideoCapture(0)

while True:
	# Capture frame-by-frame
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# get width and length of the video stream
	frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
	frame_length = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

	faces = face_cascade.detectMultiScale(
	gray,
	scaleFactor=1.1,
	minNeighbors=5,
	minSize=(30, 30),
	flags=cv2.CASCADE_SCALE_IMAGE
	)

	# draw a circle at the center point of the screen
	cv2.circle(frame, (int(frame_width/2), int(frame_length/2)), search_radius, (255, 0, 0), 2)

	# draw a black rectangle behind the text
	cv2.rectangle(frame, (0, 0), (325, 110), (0, 0, 0), -1)

	# display text that shows the coords for the center of the screen
	frame_mid_x = frame_width/2
	frame_mid_y = frame_length/2
	cv2.putText(frame, (f'Frame Center Point: ({frame_mid_x}, {frame_mid_y})'), (10, 25), font, font_size, main_font_color)
	
	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		center_point_x = int((2*x + w)/2)
		center_point_y = int((2*y + h)/2)

		# find the center point of the rectangle: remeber, it's BRG
		cv2.circle(frame, (center_point_x, center_point_y), 5, (0, 0, 255), -1)

		# display center coords for easy debugging later
		cv2.putText(frame, (f'Center Point: ({center_point_x}, {center_point_y})'), (10, 50), font, font_size, blue_font_color)

		# display text that show the delta x and y between the center of the face and the center of the screen
		delta_x = frame_mid_x - center_point_x
		delta_y = frame_mid_y - center_point_y
		cv2.putText(frame, (f'Deltas: ({delta_x}, {delta_y})'), (10, 75), font, font_size, green_font_color)

		# calculate the area of the rectangle over the face -- changes in this value over time will tell us whether the person is moving towards or away from the camera
		face_width = w
		face_height = h

		face_area = (w * h)/10000
		cv2.putText(frame, (f'Face Area: {face_area} units^2'), (10, 100), font, font_size, red_font_color)

		# only move axis 1 if we are beyond the search radius
		if abs(delta_y) > search_radius:
			ax1_current_pos = drive_1.axis1.controller.pos_setpoint

			# modify the current position equivalent to 0.5 degrees
			if delta_y >= 0:
				ax1_current_pos += int(2917/2)
			else:
				ax1_current_pos -= int(2917/2)

			# soft locks
			if ax1_current_pos > ax1_max_lim:
				ax1_current_pos = ax1_max_lim

			if ax1_current_pos < ax1_min_lim:
				ax1_current_pos = ax1_min_lim

			drive_1.axis1.controller.pos_setpoint = ax1_current_pos

	# EVERYTHING GOES ABOVE THIS LINE #
	# Display the resulting frame
	cv2.imshow('Video', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
drive_1.axis0.controller.pos_setpoint = 0
drive_1.axis1.controller.pos_setpoint = 0
cv2.destroyAllWindows()
