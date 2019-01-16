import odrive
import time
from odrive.enums import *


ax0_min_lim = 0
ax1_min_lim = 0

ax0_max_lim = 275000
ax1_max_lim = 425000

# find the first odrive
drive_1 = odrive.find_any()

# calibrate the motors
drive_1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("now calibrating axis0")
while drive_1.axis0.current_state != AXIS_STATE_IDLE:
	time.sleep(0.1)

drive_1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("now calibrating axis1")
while drive_1.axis1.current_state != AXIS_STATE_IDLE:
	time.sleep(0.1)

# enter closed-loop control for both motors
drive_1.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
drive_1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

def position():
	ax0_pos = int(input("Enter position for axis 0: "))

	if ax0_pos > ax0_max_lim or ax0_pos < ax0_min_lim:
		print("ax0 out of range!")
		ax0_pos = 0
		position()

	ax1_pos = int(input("Enter position for axis 1: "))

	if ax1_pos > ax1_max_lim or ax1_pos < ax0_min_lim:
		print("ax1 out of range!")
		ax1_pos = 0
		position()

	drive_1.axis0.controller.pos_setpoint = ax0_pos
	print("moving to: {}".format(ax0_pos))

	drive_1.axis1.controller.pos_setpoint = ax1_pos
	print("moving to: {}".format(ax1_pos))

	ax0_current_pos = drive_1.axis0.controller.pos_setpoint 
	ax1_current_pos = drive_1.axis1.controller.pos_setpoint 

	print("axis0 position: {} \naxis1 position: {}".format(ax0_current_pos, ax1_current_pos))
	new_pos = input("new position?")

	if new_pos.lower() == "y":
		position()	
	else:
		print("returning home")
		drive_1.axis0.controller.pos_setpoint = 0
		drive_1.axis1.controller.pos_setpoint = 0
		exit()

position()
