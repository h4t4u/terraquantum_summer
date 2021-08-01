import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import math

#
# This script demonstrates errors rate and steps quantity of the graph descent method, which is
# basically our signum-gradient descent method with reduced steps and errors. It theoretically shall work 
# good in all cases, where the gradient descent is good, but can be of use in many other situations, too.
#

# Recursive check of the algorithm

def check_minimum_recursively(J, x):
	DIM = J.shape[0]
	minimum = np.dot(x.T,np.dot(J,x))

	for num in range(2**DIM):
		arr = (((num & (1 << np.arange(DIM)))) > 0).astype(int)*2-1
		if np.dot(arr.T,np.dot(J,arr)) < minimum:
			print(x, arr)
			return False
	return True

def check_maximum_recursively(J, x):
	DIM = J.shape[0]
	maximum = np.dot(x.T,np.dot(J,x))

	for num in range(2**DIM):
		arr = (((num & (1 << np.arange(DIM)))) > 0).astype(int)*2-1
		if np.dot(arr.T,np.dot(J,arr)) > maximum:
			print(x, arr)
			return False
	return True

# The algorithm realisation

def find_bottom_graph(J):
	DIM = J.shape[0]
	x = np.random.sample(DIM)
	x_scaled = np.sign(x)
	not_bottom = True

	while not_bottom:
		not_bottom = False
		min_ = np.dot(x_scaled.T,np.dot(J, x_scaled))
		x_scaled_moved = np.copy(x_scaled)

		for i in range(DIM):
			x_scaled_moved[i] *= -1
			min_candidate = np.dot(x_scaled_moved.T,np.dot(J, x_scaled_moved))

			if min_candidate < min_:
				min_ = min_candidate
				x_scaled = np.copy(x_scaled_moved)
				not_bottom = True

			x_scaled_moved[i] *= -1
	return x_scaled

def find_top_graph(J):
	DIM = J.shape[0]
	x = np.random.sample(DIM)
	x_scaled = np.sign(x*2-1)
	not_bottom = True

	while not_bottom:
		not_bottom = False
		max_ = np.dot(x_scaled.T,np.dot(J, x_scaled))
		x_scaled_moved = np.copy(x_scaled)

		for i in range(DIM):
			x_scaled_moved[i] *= -1
			max_candidate = np.dot(x_scaled_moved.T,np.dot(J, x_scaled_moved))

			if max_candidate > max_:
				max_ = max_candidate
				x_scaled = np.copy(x_scaled_moved)
				not_bottom = True

			x_scaled_moved[i] *= -1
	return x_scaled

def test():
	steps = np.zeros(18)
	errors = np.zeros(18)
	samples = 1000
	for DIM in range(2,20):
		print('DIM', DIM)
		for i in range(samples):
			J = np.random.sample((DIM, DIM))
			x = find_bottom_graph(J)
			if not check_minimum_recursively(J, x):
				errors[DIM-2] += 1

		print('errors',errors)
		print('mean steps', steps/samples)




