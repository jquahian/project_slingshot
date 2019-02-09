import odrive
import time
import degrees_calc as dc
from odrive.enums import *

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

def calibrate_all():	
	print('\n\nbeginning calibration...')

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
	print("axis 0 homed at: {} \naxis 1 homed at: {}".format(drive_1.axis0.controller.pos_setpoint, 
															 drive_1.axis1.controller.pos_setpoint))
	time.sleep(3.0)

	print("\nslingshot fully calibrated")

def home_axis():
	drive_1.axis0.controller.pos_setpoint = 0
	drive_1.axis1.controller.pos_setpoint = 0

def move_axis(axis, axis_min, axis_max, num_degrees, multiplier, speed_multi):
	
	# send commands to each joint
	if axis == 0:
		if drive_1.axis0.controller.pos_setpoint < axis_min:
			drive_1.axis0.controller.pos_setpoint = axis_min
		elif drive_1.axis0.controller.pos_setpoint > axis_max:
			drive_1.axis0.controller.pos_setpoint = axis_max
		else:
			drive_1.axis0.controller.pos_setpoint += (num_degrees * multiplier * speed_multi) 
	
	if axis == 1:
		if drive_1.axis1.controller.pos_setpoint < axis_min:
			drive_1.axis1.controller.pos_setpoint = axis_min
		elif drive_1.axis1.controller.pos_setpoint > axis_max:
			drive_1.axis1.controller.pos_setpoint = axis_max
		else:
			drive_1.axis1.controller.pos_setpoint += (num_degrees * multiplier * speed_multi)

def move_arm():
	# move all joints to specific point in space using IK
	pass
