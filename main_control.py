import odrive
import time
import degrees_calc as dc
import serial
from odrive.enums import *

# board with axis 0, 1
board_0_num = '387F37573437'

# board with axis 2, 3
board_1_num = '207C377E3548'

# board with axis 4
board_2_num = '207D37A53548'

# gear ratios
ax0_gearing = 64
ax1_gearing = 128
ax2_gearing = 64
ax3_gearing = 128
ax4_gearing = 4

# soft minimums
ax0_min_lim = -dc.return_counts(90, ax0_gearing)
ax1_min_lim = -dc.return_counts(10, ax1_gearing)
ax2_min_lim = -dc.return_counts(40, ax2_gearing)
ax3_min_lim = -dc.return_counts(0, ax3_gearing)
ax4_min_lim = -dc.return_counts(90, ax4_gearing)

# soft maximums
ax0_max_lim = dc.return_counts(90, ax0_gearing)
ax1_max_lim = dc.return_counts(25, ax1_gearing)
ax2_max_lim = dc.return_counts(180, ax2_gearing)
ax3_max_lim = dc.return_counts(115, ax3_gearing)
ax4_max_lim = dc.return_counts(90, ax4_gearing)

# centered position
ax0_centered = dc.return_counts(0, ax0_gearing)
ax1_centered = dc.return_counts(0, ax1_gearing)
ax2_centered = dc.return_counts(0, ax2_gearing)
ax3_centered = dc.return_counts(95, ax3_gearing)
ax4_centered = dc.return_counts(0, ax4_gearing)

# 1 degree movement per gear ratio
reduction_4 = dc.return_counts(1, ax4_gearing)
reduction_64 = dc.return_counts(1, ax0_gearing)
reduction_128 = dc.return_counts(1, ax1_gearing)

# find the first odrive
drive_1 = odrive.find_any(serial_number=board_0_num)
drive_2 = odrive.find_any(serial_number=board_1_num)
drive_3 = odrive.find_any(serial_number=board_2_num)

def calibrate_all():	
	print('\n\nbeginning calibration...')

	# calibrate the motors
	drive_1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("\nnow calibrating axis 0")
	while drive_1.axis0.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	drive_1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("now calibrating axis 1")
	while drive_1.axis1.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	drive_2.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("\nnow calibrating axis 2")
	while drive_2.axis0.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	drive_2.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("now calibrating axis 3")
	while drive_2.axis1.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	drive_3.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	print("\nnow calibrating axis 4")
	while drive_3.axis0.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)

	# enter closed-loop control for both motors
	print("\nentering closed-loop control")
	drive_1.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	drive_1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	drive_2.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	drive_2.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	drive_3.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	# move off of home to home position which is rougly centered
	print("\nmoving to home")
	drive_1.axis0.controller.pos_setpoint = ax0_centered
	drive_1.axis1.controller.pos_setpoint = ax1_centered
	drive_2.axis0.controller.pos_setpoint = ax2_centered
	drive_2.axis1.controller.pos_setpoint = ax3_centered
	drive_3.axis0.controller.pos_setpoint = ax4_centered

	time.sleep(1.0)

	print("\nslingshot fully calibrated")

def home_axis():
	drive_1.axis0.controller.pos_setpoint = 0
	drive_1.axis1.controller.pos_setpoint = 0
	drive_2.axis0.controller.pos_setpoint = 0
	drive_2.axis1.controller.pos_setpoint = 0
	drive_3.axis0.controller.pos_setpoint = 0

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
	if axis == 2:
		if drive_2.axis0.controller.pos_setpoint < axis_min:
			drive_2.axis0.controller.pos_setpoint = axis_min
		elif drive_2.axis0.controller.pos_setpoint > axis_max:
			drive_2.axis0.controller.pos_setpoint = axis_max
		else:
			drive_2.axis0.controller.pos_setpoint += (num_degrees * multiplier * speed_multi)
	if axis == 3:
		if drive_2.axis1.controller.pos_setpoint < axis_min:
			drive_2.axis1.controller.pos_setpoint = axis_min
		elif drive_2.axis1.controller.pos_setpoint > axis_max:
			drive_2.axis1.controller.pos_setpoint = axis_max
		else:
			drive_2.axis1.controller.pos_setpoint += (num_degrees * multiplier * speed_multi)
	if axis == 4:
		if drive_3.axis0.controller.pos_setpoint < axis_min:
			drive_3.axis0.controller.pos_setpoint = axis_min
		elif drive_3.axis0.controller.pos_setpoint > axis_max:
			drive_3.axis0.controller.pos_setpoint = axis_max
		else:
			drive_3.axis0.controller.pos_setpoint += (num_degrees * multiplier * speed_multi)

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

def move_to(index):

	# safety check
	if index < len(ax0_pos_array):
		# move the arm
		print(f"MOVING TO TARGET {index}")
		drive_1.axis0.controller.pos_setpoint = ax0_pos_array[index]
		drive_1.axis1.controller.pos_setpoint = ax1_pos_array[index]
		time.sleep(0.1)
		# while the arm is moving, do not move to the next position
		while drive_1.axis0.encoder.vel_estimate != 0 or drive_1.axis1.encoder.vel_estimate != 0:		
			time.sleep(0.1)
		else:
			# recusion
			move_to(index + 1)
	else:
		print("LAST TARGET REACHED")

# can only have one recording at a time.  This is gross as hell
def clear_recording():
	print("RECORDINGS CLEAR")
	ax0_pos_array.clear()
	ax1_pos_array.clear()