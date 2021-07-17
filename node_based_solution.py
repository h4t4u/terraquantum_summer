from rates_matrix import rates_matrix_optimized, rates_matrix, write_to_csv
from optimal_graph_algorithm import find_top_graph
import matplotlib.pyplot as plt
import numpy as np
import math

K = 4
A = 10
B = 10
rates_matrix, _ = rates_matrix_optimized([1624024010213], 'filenames', 'csv')
rates_matrix = rates_matrix[0]
z = np.zeros(K*rates_matrix.shape[1])

def func_matrix(K, rates_matrix, A, B):
	N = rates_matrix.shape[1]
	J = np.zeros((N*K, N*K))
	h = np.zeros(N*K)
	for i in range(N):
		for j in range(N):
			if i == j:
				continue
			for k in range(K):
				a = (i+k*N)%(N*K)
				b = (j+(k+1)*N)%(N*K)
				if math.isnan(rates_matrix[i][j]):
					J[a][b] -= B
					continue
				J[a][b] += math.log(rates_matrix[i, j])
				J[i+k*N][j+k*N] -= A
		for k in range(K):
			h[i+k*N] += 2*A

	print(J)
	print(h)
	return J, h

def func_to_ising(J, h):
	E = np.ones(h.size)
	J_ = 1/4*J
	h_ = (np.dot(E.T,J) + h)/2
	print(J_)
	print(h_)
	return J_, h_

def ising_to_maxcut(J, h):
    L = J.shape[0]
    J_ = np.zeros(shape = (L + 1, L + 1))
    J_[:L,:L] = J
    for i in range(L):
        J_[L , i] = h[i]/2
        J_[i, L ] = h[i]/2
    return J_
J, h = func_matrix(K, rates_matrix, A, B)
J, h = func_to_ising(J, h)
J_ = ising_to_maxcut(J, h)


print(J_)

print('starting bottom calculation')
print(find_top_graph(J_))