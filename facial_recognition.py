import numpy as np
import cv2
import math

# parts from: https://realpython.com/face-detection-in-python-using-a-webcam/

font = cv2.FONT_HERSHEY_PLAIN
font_size = 1
main_font_color = (255, 255, 255)
highlight_font_color = (0, 0, 255)

# specify correct path when changing computers
frontalface_path = 'C:/Users/Josh/Anaconda3/pkgs/opencv-3.3.1-py36h20b85fd_1/Library/etc/haarcascades/haarcascade_frontalface_default.xml'

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

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        center_point_x = int((2*x + w)/2)
        center_point_y = int((2*y + h)/2)

        # find the center point of the rectangle: remeber, it's BRG
        cv2.circle(frame, (center_point_x, center_point_y), 5, (0, 0, 255), -1)

        # display center coords for easy debugging later
        cv2.putText(frame, (f'Center Point: ({center_point_x}, {center_point_y})'), (10, 25), font, font_size, main_font_color)

    # draw a circle at the center point of the screen
    cv2.circle(frame, (int(frame_width/2), int(frame_length/2)), 5, (255, 0, 0), -1)

    # display text that shows the coords for the center of the screen
    frame_mid_x = frame_width/2
    frame_mid_y = frame_length/2
    cv2.putText(frame, (f'Frame Center Point: ({frame_mid_x}, {frame_mid_y})'), (10, 50), font, font_size, main_font_color)

    # display text that show the delta x and y between the center of the face and the center of the screen
    delta_x = frame_mid_x - center_point_x
    delta_y = frame_mid_y - center_point_y
    cv2.putText(frame, (f'Deltas: ({delta_x}, {delta_y})'), (10, 75), font, font_size, main_font_color)

    # calculate the area of the rectangle over the face -- changes in this value over time will tell us whether the person is moving towards or away from the camera
    face_width = w
    face_height = h

    face_area = (w * h)/10000
    cv2.putText(frame, (f'Face Area: {face_area} units^2'), (10, 100), font, font_size, main_font_color)

    # assume 30 units from camera... fixe value until we get a range finder
    ax_1_theta = math.degrees(np.arctan(delta_y/30))
    cv2.putText(frame, (f'AXIS 1 DEGREES TO MOVE: ({ax_1_theta})'), (10, 125), font, font_size, highlight_font_color)

    # EVERYTHING GOES ABOVE THIS LINE #
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
