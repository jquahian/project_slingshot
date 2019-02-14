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
			if axis == 4 and abs(axis_value) >= 0.15 and mc.arm_currently_moving == False:
				# move all code moving the arm into the control script
				mc.move_axis(0, 
							 mc.ax0_min_lim, 
							 mc.ax0_max_lim, 
							 mc.reduction_64,
							 1, 
							 axis_value)

			if axis == 1 and abs(axis_value) >= 0.15 and mc.arm_currently_moving == False:
				mc.move_axis(1, 
							 mc.ax1_min_lim,
							 mc.ax1_max_lim, 
							 mc.reduction_128,
							 0.5, # increases our speed by 2
							 -axis_value)

		# handle the button inputs -- output is 0/1
		for button in range(button_count):
			btn_value = joystick.get_button(button)
			# home robot and exit
			if button == 6 and btn_value == 1:
				mc.home_axis()
				done = True

			# no idea what button this is
			if button == 1 and btn_value == 1:
				mc.record_movement()

			# no idea what button this is
			if button == 2 and btn_value == 1:
				mc.playback_movement()
			
			# no idea what button this is
			if button == 3 and btn_value == 1:
				# this is a fucking stupid way to do this
				mc.clear_recording()

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
