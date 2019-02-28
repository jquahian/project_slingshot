import math

# this is for 3 DOF rotation along the Y axis
# link lengths
a_1 = 3
a_2 = 5.6568
a_3 = 5.3852

def cosine_law_angle(side_a, side_b, side_c):
	angle = math.acos((side_c**2 - side_a**2 - side_b**2) / (-2 * side_a * side_b))
	return angle

def cosine_law_length(side_a, side_b, theta):
	length = math.sqrt((side_a**2 + side_b**2) - (2 * side_a * side_b * math.cos(theta)))
	return length

# forward axis when looking straight at the arm
x = float(input("enter x value: "))

if (a_2 + a_3) < abs(x):
	print('\nout of reach on x -- re-enter x')
	x = float(input("enter x value: "))

# left to right axis when looking straight at the arm
y = float(input("\nenter y value: "))

# down to up axis when looking straight at the arm
# z is the distance from the ground plane to the WRIST JOINT, not the tip of the end-effector
z = float(input("\nenter z value: "))

print(f"x value: {x} \ny value: {y} \nz value: {z}")

r_1 = math.sqrt(x**2 + z**2)

phi_1 = math.atan(z / x)

phi_2 = math.radians(90) - phi_1

r_2 = cosine_law_length(r_1, a_1, phi_2)

phi_3 = cosine_law_angle(a_1, r_2, r_1)

phi_4 = cosine_law_angle(r_2, a_2, a_3)

theta_1 = math.radians(180) - (phi_3 + phi_4)

theta_2 = cosine_law_angle(a_2, a_3, r_2)

# first revolute joint on x-z plane
theta_1 = math.degrees(theta_1)

# second revolute joint on x-z plane
theta_2 = math.degrees(theta_2)

# base joint - first revolute joint on x-y plane
theta_3 = math.degrees(math.asin(y / x))

print(f"theta 1: {theta_1}, \ntheta 2: {theta_2} \ntheta 3: {theta_3}")
