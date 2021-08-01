from rates_matrix import rates_matrix_optimized, rates_matrix, write_to_csv, read_from_csv
import numpy as np
import math
import matplotlib.pyplot as plt

#this method uses Bellman-Ford algorithm to find non-negative cycle for prepaired dist_matrix

def bellman_ford(dist_matrix):
	dists = np.full(dist_matrix.shape[0], np.inf)
	prevs = np.full(dist_matrix.shape[0], None)
	dists[0] = 0
	for k in range(len(dists)+1):
		for i in range(dist_matrix.shape[0]):
			for j in range(dist_matrix.shape[0]):
				if math.isnan(dist_matrix[i,j]):
					continue
				if dists[i] == np.inf:
					continue
				if dists[j] > dists[i] + dist_matrix[i,j]:
					dists[j] = dists[i] + dist_matrix[i,j]
					prevs[j] = i
					if k == len(dists):
						cycle = np.array([])
						t = j
						while True:
							cycle = np.append(cycle, t).astype(np.int)
							t = prevs[cycle[-1]]
							if t in cycle:
								cycle = cycle[np.where(cycle == t)[0][0] : ]
								break
						return np.flip(cycle)

	return np.array([])

#finds the best or near-best cycle using Bellman-Ford function

def find_optimum(rates_matrix, t, currencies):
	rates_matrix = -np.log(rates_matrix.astype('float64')) + np.log(1.00002)
	cycle = bellman_ford(rates_matrix[t])

	for j in range(9):
		if bellman_ford(rates_matrix[t] + np.log(1.00002)*j).size != 0:
			cycle = bellman_ford(rates_matrix[t] + np.log(1.00002)*j)
		else:
			break

	return np.append(cycle, cycle[0])


