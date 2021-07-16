from rates_matrix import rates_matrix_optimized, rates_matrix, write_to_csv
import matplotlib.pyplot as plt
import numpy as np
import math

CYCLES_NUM = 3
NUM = 100
FILENAMES_FILE = 'filenames'
CSV_DIR = 'csv'
timestamps = np.array([1624024010213 + i * 1000 for i in range(100)])
rates_matrix, currencies = rates_matrix_optimized(timestamps, FILENAMES_FILE, CSV_DIR)
write_to_csv(rates_matrix, currencies, 0, 'result.csv')

print(currencies)
AMOUNT = 1000000

def cycle_count_integer(way, t, value):
	currencies
	for k in range(len(way)-1):
		currency = way[k]
		next_currency = way[k+1]
		try:
			i = np.where(currencies == currency)[0]
			j = np.where(currencies == next_currency)[0]
			value *= rates_matrix[t,i,j]
			value = int(value)
			if math.isnan(rates_matrix[t,i,j]):
				print('You cannot buy', currency, 'for', next_currency)
		except ValueError:
			print('Wrong cycle: one of the currencies isn\'t available:', currency, next_currency)
			return AMOUNT
	return value

def recursive_find_cycle_integer(way, value, t):
    if len(way) > 5:
        return
    if len(way) > 1 and way[-1] == way[0]:
        cycle_currencies = np.take(currencies, way)
        #print(value, cycle_currencies)
        if value >= AMOUNT:
            print('!!!', value, cycle_currencies)
        return

    for i in range(len(currencies)):
        if math.isnan(rates_matrix[t, way[-1], i]):
            continue
        if i in way[1:]:
            continue
        recursive_find_cycle_integer(np.append(way,i), int(value*rates_matrix[t, way[-1], i]*(1-0.2*0.01*0.01)), t)

def check_cycles(cycle):
	income = np.ones((NUM, CYCLES_NUM))*AMOUNT

	file = open('income2', 'wt')

	for i in range(NUM):
		for j in range(CYCLES_NUM):
			income[i,j] = cycle_count_integer(cycle[j], i, AMOUNT)

	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot()
	ax.set_xlabel('time, s')
	ax.set_ylabel('income per cycle, base points')
	ax.set_title('data for 5-node cycle, initial amount ' + str(AMOUNT) + ' ')
	file.write(str(income))

	for j in range(CYCLES_NUM):
		plt.plot((timestamps-1624024010213)/1000, (income[:,j]-AMOUNT)/AMOUNT*10000, label = str(cycle[j][:-1]))
	plt.legend()
	plt.show()


