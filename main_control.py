import odrive
import time
from odrive.enums import *

#soft minimums
ax0_min_lim = 0
ax1_min_lim = 0

# soft maximums
ax0_max_lim = 262144 # 180 degrees of rotation
ax1_max_lim = 393216 # 135 degrees of rotation

# centered position
ax0_centered = 95000
ax1_centered = 200000

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
	print("axis 0 homed at: {} \naxis 1 homed at: {}".format(ax0_centered, ax1_centered))
	time.sleep(3.0)

	print("\nslingshot fully calibrated")

def move_axis(axis_num, multiplier):
	pass
