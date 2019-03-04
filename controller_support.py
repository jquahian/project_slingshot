import pygame
import main_control as mc

mc.calibrate_all()

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

a_btn_down = False
b_btn_down = False
x_btn_down = False
start_btn_down = False

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
			if axis == 0 and abs(axis_value) >= 0.70 and mc.arm_currently_moving == False:
				mc.move_axis(0, 
							 mc.ax0_min_lim,
							 mc.ax0_max_lim, 
							 mc.reduction_64,
							 0.5,
							 -axis_value)

			if axis == 1 and abs(axis_value) >= 0.70 and mc.arm_currently_moving == False:
				mc.move_axis(1, 
							 mc.ax1_min_lim,
							 mc.ax1_max_lim, 
							 mc.reduction_128,
							 0.30,
							 -axis_value)

			if axis == 4 and abs(axis_value) >= 0.70 and mc.arm_currently_moving == False:
				# move all code moving the arm into the control script
				mc.move_axis(2, 
							 mc.ax2_min_lim, 
							 mc.ax2_max_lim, 
							 mc.reduction_64,
							 0.50, 
							 -axis_value)

			if axis == 3 and abs(axis_value) >= 0.70 and mc.arm_currently_moving == False:
				# move all code moving the arm into the control script
				mc.move_axis(3, 
							 mc.ax3_min_lim, 
							 mc.ax3_max_lim, 
							 mc.reduction_128,
							 0.5, 
							 -axis_value)
			
			if axis == 2 and abs(axis_value) >= 0.15 and mc.arm_currently_moving == False:
				# move all code moving the arm into the control script
				mc.move_axis(4, 
							 mc.ax4_min_lim, 
							 mc.ax4_max_lim, 
							 mc.reduction_4,
							 1.5, 
							 -axis_value)

		# handle the button inputs -- output is 0/1
		for button in range(button_count):
			btn_value = joystick.get_button(button)
			# home robot and exit
			if button == 6 and btn_value == 1:
				print("RETURNING HOME AND EXITING")
				mc.home_axis()
				done = True

			# A button
			if button == 0 and btn_value == 1 and a_btn_down == False:
				mc.record_movement()
				a_btn_down = True
			elif button == 0 and btn_value == 0 and a_btn_down == True:
				a_btn_down = False

			# start button
			if button == 7 and btn_value == 1 and start_btn_down == False:
				start_btn_down = True
				mc.move_to(0)
			elif button == 7 and btn_value == 0 and start_btn_down == True:
				start_btn_down = False

			# B button
			if button == 1 and btn_value == 1 and b_btn_down == False:
				# this is a fucking stupid way to do this
				if len(mc.ax0_pos_array) != 0: 
					mc.clear_recording()

			# X button
			if button ==3 and btn_value == 1 and b_btn_down == False:
				# trigger a flag to loop through the list of saved positions again
				x_btn_down = True
			elif button == 3 and btn_value == 0 and a_btn_down == True:
				x_btn_down = False

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
