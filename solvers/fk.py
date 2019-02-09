import numpy as np
import math

# rotation matricies
def z_rot_matrix(theta):
	zmat = [[np.cos(theta), -np.sin(theta), 0],
			[np.sin(theta), np.cos(theta), 0],
			[0, 0, 1]]
	return zmat

one_id = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# joint angles entered in degrees but converted to radians
t1 = math.radians(25)
t2 = math.radians(30)
t3 = math.radians(45)
t4 = math.radians(20)
t5 = math.radians(21)
t6 = math.radians(10)

r0_1 = np.matmul(z_rot_matrix(t1), [[1, 0, 0], [0, 0, -1], [0, 1, 0]])
r1_2 = np.matmul(z_rot_matrix(t2), one_id)
r2_3 = np.matmul(z_rot_matrix(t3), [[0, 0, 1], [1, 0, 0], [0, 1, 0]])
r3_4 = np.matmul(z_rot_matrix(t4), [[1, 0, 0], [0, 0, -1], [0, 1, 0]])
r4_5 = np.matmul(z_rot_matrix(t5), [[1, 0, 0], [0, 0, 1], [0, -1, 0]])
r5_6 = np.matmul(z_rot_matrix(t6), one_id)

rotation_matrices = [r0_1, r1_2, r2_3, r3_4, r4_5, r5_6]

for i in range(len(rotation_matrices) - 1):
	r0_6 = rotation_matrices[i] @ rotation_matrices[i+1]
	
# print(r0_6)

# displacement vector calculation
# distances from joint n to joint n + 1 in mm
a1 = 10
a2 = 10
a3 = 10
a4 = 10
a5 = 10
a6 = 10

# MAYBE THIESE DISPLACMENT FRAMES ARE CORRECT??
d0_1 = [[0], [0], [a1]]
d1_2 = [[a2 * np.cos(t1)], [a2 * np.sin(t1)], [0]]
d2_3 = [[a3 * np.cos(t2)], [a3 * np.sin(t2)], [0]]
d3_4 = [[0], [0], [a4]]
d4_5 = [[a5 * np.sin(t4)], [a5 * np.cos(t4)], [0]]
d5_6 = [[0], [0], [a6]]

displacement_matrices = [d0_1, d1_2, d2_3, d3_4, d4_5, d5_6]

# Homogenous Transformation Matrix
# Here, we combine rotation matrix and displacement matrix
# np.concatenate((rotation matrix, displacement matrix), position)
h0_1 = np.concatenate((r0_1, d0_1), 1)

# make our homogenous matrix a square again where h0_1 is on top of the [0,0,0,1] filler row
h0_1 = np.concatenate((h0_1, [[0, 0, 0, 1]]), 0)

homogenous_matrices = []

for i in range(len(rotation_matrices)):
	h0 = np.concatenate((rotation_matrices[i], displacement_matrices[i]), 1)
	h0 = np.concatenate((h0, [[0, 0, 0, 1]]), 0)
	homogenous_matrices.append(h0)

for i in range(len(homogenous_matrices) - 1):
	h0_6 = homogenous_matrices[i] @ homogenous_matrices[i + 1]

item = 5

# print('\nrotation matrix: \n{} \n\ndisplacement matrix: \n{} \n\nhomogenous matrix: \n{}'.format(rotation_matrices[item], displacement_matrices[item], homogenous_matrices[item]))

print(h0_6)