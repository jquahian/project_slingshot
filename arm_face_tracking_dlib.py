# lots of code based on tutorials from: https://www.pyimagesearch.com/

# USAGE
# python arm_face_tracking_dlib.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python arm_face_tracking_dlib.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance as dist
import time
import argparse
import imutils
import dlib
import cv2
import math
import main_control as mc

video_width = 1000

head_vertical_threshold = 25
head_horizontal_threshold = 25
head_rotation_threshold = 15

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
 
mc.calibrate_all()

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 200 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, video_width)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	frame_height = frame.shape[0]
	frame_width = frame.shape[1]

	frame_mid_x = int(frame_width / 2)
	frame_mid_y = int(frame_height / 2)

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

		eye_theta = math.degrees(math.atan(delta_y / delta_x))

		# face bounding box
		(x, y, w, h) = face_utils.rect_to_bb(rect)	
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# find the center of our face bounding box
		face_mid_x  = int(x + w / 2)
		face_mid_y = int(y + h / 2)

		cv2.circle(frame, (face_mid_x, face_mid_y), 1, (0, 255, 255), -1)

		face_vert_displacement = frame_mid_y - face_mid_y
		face_hor_displacement = frame_mid_x - face_mid_x

		# move the arm to match the vertical displacement of the face
		if abs(face_vert_displacement) > head_vertical_threshold:
			if face_vert_displacement > 0:
				speed_direction = 0.85
			else:
				speed_direction = -0.85
			mc.move_axis(3, 
						 mc.ax3_min_lim, 
						 mc.ax3_max_lim,
						 mc.reduction_128,
						 1,
						 speed_direction)

		# move the arm to match the horizontal displacement of the face
		if abs(face_hor_displacement) > head_horizontal_threshold:
			if face_hor_displacement > 0:
				speed_direction = -0.9
			else:
				speed_direction = 0.9
			mc.move_axis(0, 
						 mc.ax0_min_lim, 
						 mc.ax0_max_lim,
						 mc.reduction_64,
						 1,
						 speed_direction)

		# move the arm to match the rotational displacement of the face
		if abs(eye_theta) >= head_rotation_threshold:
			if eye_theta > 0:
				speed_direction = 10
			else:
				speed_direction = -10
			mc.move_axis(4,
						 mc.ax4_min_lim, 
						 mc.ax4_max_lim,
						 mc.reduction_4,
						 1,
						 speed_direction)

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
cv2.destroyAllWindows()
vs.stop()
time.sleep(1.0)
mc.home_axis()
