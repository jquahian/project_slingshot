import odrive
import time
from odrive.enums import *

#soft minimums
ax0_min_lim = 0
ax1_min_lim = 0

# soft maximums
ax0_max_lim = 262144 # 180 degrees of rotation
ax1_max_lim = 393216 # 135 degrees of rotation

# gear ratios for the axis
ax0_gearing = 128
ax1_gearing = 64

# encoder counts per revolution
encoder_cpr = 8192

# centered position
ax0_centered = 90000
ax1_centered = 200000

print('\n\nbeginning calibration...')
# find the first odrive
drive_1 = odrive.find_any()

# calibrate the motors
drive_1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("\nnow calibrating axis 0")
while drive_1.axis0.current_state != AXIS_STATE_IDLE:
	time.sleep(0.1)

drive_1.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
print("now calibrating axis 1")
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

# options to operate the arm
def options():
	print("\nselect command:")
	sel = input("(a) position control \n(b) center \n(c) home \n(d) exit \nCOMMAND: ")
	if sel.lower() == 'a':
		position()
	elif sel.lower() == 'b':
		movement(ax0_centered, ax1_centered)
	elif sel.lower() == 'c':
		movement(ax0_min_lim, ax1_min_lim)
	else:
		exit_control()

# set the absolute position manually
def position():
	ax0_degs = int(input("\nEnter position for axis 0: "))
	ax0_counts = int((ax0_degs / 360) * (ax0_gearing * encoder_cpr))

	if ax0_counts > ax0_max_lim or ax0_counts < ax0_min_lim:
		print("axis 0 out of range!")
		ax0_counts = 0
		position()

	ax1_degs = int(input("Enter position for axis 1: "))
	ax1_counts = int((ax1_degs / 360) * (ax1_gearing * encoder_cpr))

	if ax1_counts > ax1_max_lim or ax1_counts < ax0_min_lim:
		print("axis 1 out of range!")
		ax1_counts = 0
		position()

	movement(ax0_counts, ax1_counts)

# move the arm
def movement(ax0_counts, ax1_counts):
	drive_1.axis0.controller.pos_setpoint = ax0_counts
	print("\nmoving to: {}".format(ax0_counts))

	drive_1.axis1.controller.pos_setpoint = ax1_counts
	print("moving to: {}".format(ax1_counts))

	ax0_current_pos = (drive_1.axis0.controller.pos_setpoint/(ax0_gearing * encoder_cpr) * 360) 
	ax1_current_pos = (drive_1.axis1.controller.pos_setpoint/(ax1_gearing * encoder_cpr) * 360)  

	print("\naxis 0 position: {} \naxis 1 position: {}".format(ax0_current_pos, ax1_current_pos))

	options()

def exit_control():
	print("\nreturning home")
	drive_1.axis0.controller.pos_setpoint = 0
	drive_1.axis1.controller.pos_setpoint = 0
	exit()

options()
