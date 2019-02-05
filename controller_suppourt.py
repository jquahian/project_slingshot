import pygame
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
ax0_gearing = 64
ax1_gearing = 128

# encoder counts per revolution
encoder_cpr = 8192

# centered position
ax0_centered = 95000
ax1_centered = 200000

print('\n\nbeginning calibration...')
# find the first odrive
drive_1 = odrive.find_any()

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

# initialize pygame
pygame.init()

# flag to say when the 'game' is done
done = False

# some window size
size = [300, 500]

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

# initialize the joystick
pygame.joystick.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class TextPrint:
	def __init__(self):
		self.reset()
		self.font = pygame.font.Font(None, 20)

	def print(self, screen, textString):
		textBitmap = self.font.render(textString, True, BLACK)
		screen.blit(textBitmap, [self.x, self.y])
		self.y += self.line_height
		
	def reset(self):
		self.x = 10
		self.y = 10
		self.line_height = 15
		
	def indent(self):
		self.x += 10
		
	def unindent(self):
		self.x -= 10

textPrint = TextPrint()

while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	screen.fill(WHITE)
	textPrint.reset()
	joystick_count = pygame.joystick.get_count()

	for i in range(joystick_count):
		# initialize our joystick
		joystick = pygame.joystick.Joystick(i)
		joystick.init()

		joystick_count = pygame.joystick.get_count()
		button_count = joystick.get_numbuttons()
		axes_count = joystick.get_numaxes()
		dpad_count = joystick.get_numhats()

		textPrint.print(screen, "Joystick {}".format(i) )
		textPrint.indent()
	
		# Get the name from the OS for the controller/joystick
		name = joystick.get_name()
		textPrint.print(screen, "Joystick name: {}".format(name) )
		
		# Usually axis run in pairs, up/down for one, and left/right for
		# the other.
		axes = joystick.get_numaxes()
		textPrint.print(screen, "Number of axes: {}".format(axes) )
		textPrint.indent()
		
		# handle axis inputs
		for axis in range(axes_count):
			axis_value = joystick.get_axis(axis)
			textPrint.print(screen, "Axis {} value: {:>6.3f}".format(axis, axis_value))
			# MOVE AXIS HERE
			if axis == 0 and abs(axis_value) >= 0.15:
				a += 1 * axis_value
				print(a)

		# handle the button inputs -- output is 0/1
		for button in range(button_count):
			btn_value = joystick.get_button(button)
			if button == 6 and btn_value == 1:
				done = True
			textPrint.print(screen, "Btn {} value: {}".format(button, btn_value))

		# handle the D pad inputs
		# up (0, 1)
		# right (1, 0)
		# down (0, -1)
		# left(-1, 0)
		for dpad in range(dpad_count):
			dpad_value = joystick.get_hat(dpad)
			textPrint.print(screen, "D-pad {} value: {}".format(dpad, dpad_value))

	pygame.display.flip()

	clock.tick(60)

# to prevent the program from hanging
pygame.quit()
