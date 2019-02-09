import odrive
import time
from odrive.enums import *
import degrees_calc as dc

# gear ratios
ax0_gearing = 64
ax1_gearing = 128

# soft minimums
ax0_min_lim = 0
ax1_min_lim = 0

# soft maximums
ax0_max_lim = dc.return_counts(180, ax0_gearing)
ax1_max_lim = dc.return_counts(135, ax1_gearing)

# centered position
ax0_centered = dc.return_counts(65, ax0_gearing)
ax1_centered = dc.return_counts(70, ax1_gearing)

# 1 degree movement per gear ratio
reduction_64 = dc.return_counts(1, ax0_gearing)
reduction_128 = dc.return_counts(1, ax1_gearing)

# find the first odrive
drive_1 = odrive.find_any()

ax0_req_state = drive_1.axis0.requested_state
ax1_req_state = drive_1.axis1.requested_state

ax0_pos = drive_1.axis0.controller.pos_setpoint
ax1_pos = drive_1.axis1.controller.pos_setpoint

def calibrate_all():	
	print('\n\nbeginning calibration...')

	# calibrate the motors
	ax0_req_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("\nnow calibrating axis 0")
	while ax0_req_state != AXIS_STATE_IDLE:
		time.sleep(3.0)

	ax1_req_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("now calibrating axis 1")
	while ax1_req_state != AXIS_STATE_IDLE:
		time.sleep(3.0)

	# enter closed-loop control for both motors
	print("\nentering closed-loop control")
	ax0_req_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	ax1_req_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	# move off of home to home position which is rougly centered
	print("\nmoving to home")
	ax0_pos = ax0_centered
	ax1_pos = ax1_centered
	print("axis 0 homed at: {} \naxis 1 homed at: {}".format(ax0_pos, ax1_pos))
	time.sleep(3.0)

	print("\nslingshot fully calibrated")

def home_axis():
	ax0_pos = 0
	ax1_pos = 0

def move_axis(axis, axis_min, axis_max, num_degrees, multiplier):
	# send commands to each joint

	if axis < axis_min:
		axis = axis_min
	elif axis > axis_max:
		axis = axis_max
	else:
		axis += ((int(2917/2) * multiplier)) 

def move_arm():
	# move all joints to specific point in space
	pass
