import math

a_1 = 3
a_2 = 5.6568
a_3 = 5.3852

# forward axis when looking straight at the arm
x = int(input("enter x value: "))

if (a_2 + a_3) < abs(x):
	print('\nout of reach on x -- re-enter x')
	x = int(input("enter x value: "))

# left to right axis when looking straight at the arm
y = int(input("\nenter y value: "))

# down to up axis when looking straight at the arm
# z is the distance from the ground plane to the WRIST JOINT, not the tip of the end-effector
z = int(input("\nenter z value: "))

print(f"x value: {x} \ny value: {y} \nz value: {z}")

r_1 = math.sqrt(x**2 + z**2)

phi_1 = math.atan(z/x)

phi_2 = math.radians(90) - phi_1

r_2 = math.sqrt(r_1**2 + a_1**2 - 2 * r_1 * a_1 * math.cos(phi_2))

phi_3 = math.acos((r_1**2 - a_1**2 - r_2**2)/(-2*a_1*r_2))

phi_4 = math.acos((a_3**2 - r_2**2 - a_2**2)/(-2*r_2*a_2))

theta_1 = math.radians(180) - (phi_3 + phi_4)

theta_2 = math.acos((r_2**2 - a_2**2 - a_3**2)/(-2*a_2*a_3))

# first revolute joint on x-z plane
theta_1 = math.degrees(theta_1)

# second revolute joint on x-z plane
theta_2 = math.degrees(theta_2)

# base joint - first revolute joint on x-y plane
theta_3 = math.degrees(math.acos(y/x))

print(f"theta 1: {theta_1}, \ntheta 2: {theta_2} \ntheta 3: {theta_3}")
