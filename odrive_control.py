import odrive
import time
from odrive.enums import *

#soft minimums
ax0_min_lim = 0
ax1_min_lim = 0

# soft maximums
ax0_max_lim = 275000
ax1_max_lim = 425000

# centered position
ax0_centered = 90000
ax1_centered = 205000

print('\n\nbeginning calibration...')
# find the first odrive
drive_1 = odrive.find_any()

# calibrate the motors
drive_1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("\nnow calibrating axis0")
while drive_1.axis0.current_state != AXIS_STATE_IDLE:
	time.sleep(0.1)

drive_1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("now calibrating axis1")
while drive_1.axis1.current_state != AXIS_STATE_IDLE:
	time.sleep(3.0)

# enter closed-loop control for both motors
print("\nentering closed-loop control")
drive_1.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
drive_1.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# move off of home to center
print("\nmoving to center")
drive_1.axis0.controller.pos_setpoint = ax0_centered
drive_1.axis1.controller.pos_setpoint = ax1_centered
print("axis 0 centered at: {} \naxis 1 centered at: {}".format(ax0_centered, ax1_centered))
time.sleep(3.0)

def position():
	ax0_pos = int(input("\nEnter position for axis 0: "))

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
	print("\nmoving to: {}".format(ax0_pos))

	drive_1.axis1.controller.pos_setpoint = ax1_pos
	print("moving to: {}".format(ax1_pos))

	ax0_current_pos = drive_1.axis0.controller.pos_setpoint 
	ax1_current_pos = drive_1.axis1.controller.pos_setpoint 

	print("\naxis0 position: {} \naxis1 position: {}".format(ax0_current_pos, ax1_current_pos))
	new_pos = input("\nnew position?")

	if new_pos.lower() == "y":
		position()	
	else:
		print("\nreturning home")
		drive_1.axis0.controller.pos_setpoint = 0
		drive_1.axis1.controller.pos_setpoint = 0
		exit()

position()
