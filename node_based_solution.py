from rates_matrix import rates_matrix_optimized, rates_matrix, write_to_csv, read_from_csv
from optimal_graph_algorithm import find_top_graph, check_maximum_recursively
import matplotlib.pyplot as plt
import numpy as np
import math

NUM = 1000
K = 3
A = 7
B = 6

timestamps = np.array([1624024010213 + i * 1000 for i in range(NUM)])
rates_matrix = np.load('data.npy')
currencies = np.load('currencies.npy')
z = np.zeros(K*rates_matrix.shape[1])

def check_maximum_recursively_nodewise(J, x):
	DIM = J.shape[0]
	maximum = np.dot(x.T,np.dot(J,x))

	for num in range((DIM/K)**K):
		arr = (((num & (1 << np.arange(DIM)))) > 0).astype(int)*2-1
		if np.dot(arr.T,np.dot(J,arr)) > maximum:
			print(x, arr)
			return False
	return True

def func_matrix(K, rates_matrix, A, B):
	N = rates_matrix.shape[1]
	J = np.zeros((N*K, N*K))
	h = np.zeros(N*K)
	for i in range(N):
		for j in range(N):
			for k in range(K):
				a = (i+k*N)
				b = (j+(k+1)*N)%(K*N)
				if math.isnan(rates_matrix[i][j]):
					J[a][b] -= B
				else:
					J[a][b] += math.log(rates_matrix[i, j])
				J[i+k*N][j+k*N] -= A
		for k in range(K):
			h[i+k*N] += 2*A
	return J, h

def func_to_ising(J, h):
	E = np.ones(h.size)
	J_ = 1/4*J
	h_ = np.dot(E, J)/4 + np.dot(E, J.T)/4 + h/2
	return J_, h_

def ising_to_maxcut(J, h):
	L = J.shape[0]
	J_ = np.zeros(shape = (L + 1, L + 1))
	J_[:L,:L] = J
	for i in range(L):
		J_[L , i] = h[i]/2
		J_[i, L ] = h[i]/2

	return J_

N = rates_matrix.shape[1]
income = np.zeros(NUM)
for j in range(100):
	print(j)
	J, h = func_matrix(K, rates_matrix[j], A, B)
	J, h = func_to_ising(J, h)
	J_ = ising_to_maxcut(J, h)

	maximum = 0
	result = np.zeros(J_.shape[0])
	for num in range(1000):
		x = find_top_graph(J_)
		if np.dot(x.T,np.dot(J_,x)) > maximum:
			maximum = np.dot(x.T,np.dot(J_,x))
			result = x
	cycle = np.array([])

	for i in range(K):
		cycle = np.append(cycle, np.where(result[len(currencies)*i:len(currencies)*(i+1)] == result[-1])[0][0]%(len(currencies))).astype(np.int)
	income_ = 1
	for i in range(1, K+1):
		income_ *= rates_matrix[j, cycle[i%K], cycle[i-1]] * 0.99998
	if math.isnan(income_):
		print('AAA')
		income_ = 1

	income[j] = income_
	print(cycle)

	print(np.array(currencies)[cycle.astype(np.int)])

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot()
ax.set_xlabel('time, s')
ax.set_ylabel('income per cycle, base points')
ax.set_title('Node-based algorythm')
plt.plot((timestamps-timestamps[0])/1000, (income[:]-1)*10000, label = 'node-based')

plt.legend()
plt.show()
