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
		time.sleep(1.0)

	drive_1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("now calibrating axis 1")
	while drive_1.axis1.current_state != AXIS_STATE_IDLE:
		time.sleep(1.0)

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
	time.sleep(1.0)

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

def move_ik():
	# move all joints to specific point in space using IK
	pass

ax0_pos_array = []
ax1_pos_array = []

def record_movement():
	# move the joints manually with the controller
	# at each point, save positions of each joint in an array
	# then iterate through each array using a for loop to position each joint
	ax0_pos_array.append(drive_1.axis0.controller.pos_setpoint)
	ax1_pos_array.append(drive_1.axis1.controller.pos_setpoint)
	print("POSITION SAVED")

arm_currently_moving = False

target_index_position = 0
def move_to():

	# if AXIS_STATE_IDLE for all joints, move to the next point
	if drive_1.axis0.current_state == AXIS_STATE_IDLE and drive_1.axis1.current_state == AXIS_STATE_IDLE:
		if target_index_position < len(ax0_pos_array):
			arm_currently_moving = True
			print(f"MOVING TO POSITION {target_index_position}")
			drive_1.axis0.controller.pos_setpoint = ax0_pos_array[target_index_position]
			drive_1.axis1.controller.pos_setpoint = ax1_pos_array[target_index_position]
			target_index_position += 1
			move_to()
		else:
			print("FINAL POSITION REACHED")
			arm_currently_moving = False
			target_index_position = 0
	else:
		# poll the arm to see if the joints are still moving
		time.sleep(0.1)
		move_to()

# can only have one recording at a time.  This is gross as hell
def clear_recording():
	print("RECORDINGS CLEAR")
	ax0_pos_array = []
	ax1_pos_array = []