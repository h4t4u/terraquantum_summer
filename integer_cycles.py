from rates_matrix import rates_matrix_optimized, rates_matrix, write_to_csv
import matplotlib.pyplot as plt
import numpy as np
import math

def cycle_count_integer(rates_matrix, currencies, way, t, value):
	leftovers = 0
	init_currency_index = np.where(currencies == way[0])[0]
	init_amount = value
	for k in range(len(way)-1):
		currency = way[k]
		next_currency = way[k+1]
		try:
			i = np.where(currencies == currency)[0]
			j = np.where(currencies == next_currency)[0]

			value *= rates_matrix[t,i,j]
			if not math.isnan(np.asscalar(rates_matrix[t,j,init_currency_index]*(value%1))):
				leftovers += np.asscalar(rates_matrix[t,j,init_currency_index]*(value%1))

			value = int(value)

			if not math.isnan(np.asscalar(rates_matrix[t,j,init_currency_index])):
				leftovers -= value*(0.2*0.01*0.01)*rates_matrix[t,j,init_currency_index]

			if math.isnan(rates_matrix[t,i,j]):
				print('You cannot buy', currency, 'for', next_currency)

		except ValueError:
			print('Wrong cycle: one of the currencies isn\'t available:', currency, next_currency)
			return init_amount

	return value + leftovers

#The method calculates income matrix according to given cycle, varying initial amount

def count_accumulated_income_cycle(rates_matrix, currencies, cycle):
	income = np.zeros((NUM, 8))
	for j in range(8):
		amount = 100*10**j
		income[0,j] = amount
		for i in range(1,NUM):
			income[i,j] = max(cycle_count_integer(rates_matrix, currencies, cycle, i, income[i-1,j]), income[i-1,j])
	return income

#The method calculates incomes according to given cycles and initial amount

def count_accumulated_income_array(rates_matrix, currencies, cycles, initial_amount):
	income = np.zeros((NUM, cycles.shape[0]))
	for j in range(cycles.shape[0]):
		income[0,j] = initial_amount
		for i in range(1,NUM):
			income[i,j] = max(cycle_count_integer(rates_matrix, currencies, cycles[j], i, income[i-1,j]), income[i-1,j])

	print(income)
	return income

#Plotting the income

def plot_accumulated_income_cycle(timestamps, income, cycle):
	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot()
	ax.set_xlabel('time, s')
	ax.set_ylabel('integral income, base points')
	ax.set_title('data for ' + str(cycle.size) + '-node cycle ' + str(cycle[:-1]))

	for j in range(8):
		amount = 100*10**j
		plt.plot((timestamps-timestamps[0])/1000, (income[:,j]-amount)/amount*10000, label = str(amount) + 'USD')
	plt.legend()
	plt.show()

def plot_accumulated_income_array(timestamps, income, cycles):
	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot()
	ax.set_xlabel('time, s')
	ax.set_ylabel('integral income, base points')
	ax.set_title('data for ' + str(cycles.shape[1]-1) + '-node cycles')

	for j in range(cycles.shape[0]):
		amount = income[0,j]
		plt.plot((timestamps-timestamps[0])/1000, (income[:,j]-amount)/amount*10000, label = str(cycles[j]))
	plt.legend()
	plt.show()

