import numpy as np
from enum import Enum
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import math

#
# This script demonstrates errors rate and steps quantity of the graph descent method, which is
# basically our signum-gradient descent method with reduced steps and errors. It theoretically shall work 
# good in all cases, where the gradient descent is good, but can be of use in many other situations, too.
#

class Type(Enum):
	maximum = 'max',
	minimum = 'min'

# Recursive check of the vector, type  = Type.maximum/Type.minimum

def check_extremum_recursively(J, x, type):
	DIM = J.shape[0]
	extr = np.dot(x.T,np.dot(J,x))

	if type != Type.minimum and type != Type.maximum:
		raise ValueError('Wrong \'type\' variable value')

	for num in range(2**DIM):
		arr = (((num & (1 << np.arange(DIM)))) > 0).astype(int)*2-1
		if type == Type.minimum and np.dot(arr.T,np.dot(J,arr)) < extr:
			print(x, arr)
			return False

		if type == Type.maximum and np.dot(arr.T,np.dot(J,arr)) > extr:
			print(x, arr)
			return False
	return True

# The algorithm realisation

def find_extremal_graph(J, type):
	DIM = J.shape[0]
	x = np.random.sample(DIM)
	x_scaled = np.sign(x)
	not_extremal = True

	if type != Type.minimum and type != Type.maximum:
		raise ValueError('Wrong \'type\' variable value')

	while not_extremal:
		not_extremal = False
		extr = np.dot(x_scaled.T,np.dot(J, x_scaled))
		x_scaled_moved = np.copy(x_scaled)

		for i in range(DIM):
			x_scaled_moved[i] *= -1
			extr_candidate = np.dot(x_scaled_moved.T,np.dot(J, x_scaled_moved))

			if type == Type.minimum and extr_candidate < extr:
				extr = extr_candidate
				x_scaled = np.copy(x_scaled_moved)
				not_extremal = True

			if type == Type.maximum and extr_candidate > extr:
				extr = extr_candidate
				x_scaled = np.copy(x_scaled_moved)
				not_extremal = True


			x_scaled_moved[i] *= -1
	return x_scaled

def test():
	errors = np.zeros(10)
	samples = 1000
	for DIM in range(2,12):
		print('DIM', DIM)
		for i in range(samples):
			J = np.random.sample((DIM, DIM))
			x = find_extremal_graph(J, Type.minimum)
			if not check_extremum_recursively(J, x, Type.minimum):
				errors[DIM-2] += 1

		print('errors', errors)