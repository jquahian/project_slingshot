# USAGE
# python arm_face_tracking_dlib.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python arm_face_tracking_dlib.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
from odrive.enums import *
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import math
import odrive
import time


#soft minimums
ax0_min_lim = 0
ax1_min_lim = 0

# soft maximums
ax0_max_lim = 262144 # 180 degrees of rotation
ax1_max_lim = 393216 # 135 degrees of rotation

# centered position
ax0_centered = 95000
ax1_centered = 250000

video_width = 300

head_vertical_threshold = 15

head_rotation_threshold = 10

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

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
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, video_width)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	frame_height = frame.shape[0]
	frame_width = frame.shape[1]

	frame_mid_x = int(frame_width/2)
	frame_mid_y = int(frame_height/2)

	cv2.circle(frame, (frame_mid_x, frame_mid_y), head_vertical_threshold, (255, 0, 0), 1)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)
	
	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# segmented index of points outlining the right eye
		rightEye = shape[rStart:rEnd]
		rightEyeHull = cv2.convexHull(rightEye)

		# return the x,y coordinates for the two horizontal (corner) eye markers
		# medial point
		eye_x_one = rightEyeHull[0][0][0]
		eye_y_one = rightEyeHull[0][0][1]

		#lateral point
		eye_x_two = rightEyeHull[3][0][0]
		eye_y_two = rightEyeHull[3][0][1]

		# draw a line between the two eye points for reference
		eye_diagonal = cv2.line(frame, (eye_x_one, eye_y_one), (eye_x_two, eye_y_two), (0, 0, 255), 3)

		# draw a horizontal from the most lateral eye point for reference
		eye_horizontal = cv2.line(frame, (eye_x_two, eye_y_two), (eye_x_one, eye_y_two), (0, 255, 255), 1)

		# get the horizontal distance between two points
		delta_x = dist.euclidean(eye_x_one, eye_x_two)
		
		# get the vertical distance between the two points and determine if the change in angle is positive or negative
		# positive if head tilt is right, negative if left
		if eye_y_two < eye_y_one:
			delta_y = -dist.euclidean(eye_y_one, eye_y_two)
		else:
			delta_y = dist.euclidean(eye_y_one, eye_y_two)

		eye_theta = math.degrees(math.atan(delta_y/delta_x))

		# face bounding box
		(x, y, w, h) = face_utils.rect_to_bb(rect)	
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# find the center of our face bounding box
		face_mid_x  = int(x + w/2)
		face_mid_y = int(y + h/2)

		cv2.circle(frame, (face_mid_x, face_mid_y), 1, (0, 255, 255), -1)

		face_vert_displacement = frame_mid_y - face_mid_y

		# move the arm to match the vertical displacement of the face
		if abs(face_vert_displacement) > head_vertical_threshold:
			ax1_current_pos = drive_1.axis1.controller.pos_setpoint

			# modify the current position equivalent to 0.5 degrees
			if face_vert_displacement >= 0:
				ax1_current_pos += int(2917/2)
			else:
				ax1_current_pos -= int(2917/2)

			# soft locks
			if ax1_current_pos > ax1_max_lim:
				ax1_current_pos = ax1_max_lim

			if ax1_current_pos < ax1_min_lim:
				ax1_current_pos = ax1_min_lim

			drive_1.axis1.controller.pos_setpoint = ax1_current_pos

		# move the arm to match the rotational displacement of the face
		if abs(eye_theta) >= head_rotation_threshold:
			ax0_current_pos = drive_1.axis0.controller.pos_setpoint

			if eye_theta >=0:
				ax0_current_pos -= int(1456/2)
			else:
				ax0_current_pos += int(1456/2)

			# soft locks
			if ax0_current_pos > ax0_max_lim:
				ax0_current_pos = ax0_max_lim

			if ax0_current_pos < ax0_min_lim:
				ax0_current_pos = ax0_min_lim

			drive_1.axis0.controller.pos_setpoint = ax0_current_pos

		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
 
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
# reset the arm
drive_1.axis0.controller.pos_setpoint = 0
drive_1.axis1.controller.pos_setpoint = 0
cv2.destroyAllWindows()
vs.stop()
