import numpy as np
import pandas as pd

TIME_MAX_GAP = 1000 # If gap in initial csv is bigger than TIME_QUANTUM, values are not taken

def currencies_list(filenames_file):
    currencies = set()
    urls_file = open(filenames_file)
    urls = urls_file.read().splitlines()
    for url in urls:
        prefix = url[:-4]
        if len(prefix) == 6:
            currency = prefix[0:3]
            currencies.add(currency)
            currency = prefix[3:]
            currencies.add(currency)
        else:
            currencies.add(prefix)
            currencies.add('USD')
    urls_file.close()
    currencies = np.array(list(currencies))
    return currencies

### returns 3-dimensional array w/currency rates; one 2d array for each timestamp

def rates_matrix(timestamps, filenames_file, csv_dir):
    global TIME_MAX_GAP
    currencies = currencies_list(filenames_file)
    graph_table = np.full([len(timestamps),len(currencies),len(currencies)],np.nan)
    urls_file = open(filenames_file)
    urls = urls_file.read().splitlines()
    urls_file.close()

    for url in urls:
        filename = csv_dir + '/' + url
        prefix = url[:-4]
        if len(prefix) == 6:
            currency1 = prefix[0:3]
            currency2 = prefix[3:]
        else:
            currency1 = prefix
            currency2 = 'USD'
        i = np.where(currencies == currency1)[0]
        j = np.where(currencies == currency2)[0]

        graph_table[:,i,i] = 1
        graph_table[:,j,j] = 1

        df = pd.read_csv(filename)
        try:
            array = np.array(df.loc[:,'timestamp'])
            array = (array[array.astype(np.float) > 1e12])                      # defective data filtering out
            array = (array[array.astype(np.float) < 1.8e12]).astype(np.int64)   # 
            if array.max() < timestamps[0] or array.min() > timestamps[-1]:
                continue

            t = 0
            for timestamp in timestamps:
                s = df.iloc[np.argmin(np.abs(array - timestamp))]
                if abs(int(s['timestamp'])-timestamp) > TIME_MAX_GAP:
                    continue
                graph_table[t,i,j] = s['bid']
                graph_table[t,j,i] = 1/s['ask']
                t += 1
                
        except KeyError:
            print('error in file', filename, 'row:', s)

    return (graph_table, currencies)

# Does not take two-node cycles into account

def rates_matrix_optimized(timestamps, filenames_file, csv_dir):
    graph_table, currencies = rates_matrix(timestamps, filenames_file, csv_dir)
    i = 0
    while i < graph_table.shape[2]:
        array = graph_table[:, i, :]
        if np.count_nonzero(~np.isnan(array)) <= 2*len(timestamps):
            graph_table = np.delete(graph_table, i, 1)
            graph_table = np.delete(graph_table, i, 2)
            currencies = np.delete(currencies, i)

        else:
            i+=1

    return (graph_table, currencies)

def write_to_csv(rates_matrix, currencies, index, output_file):
    final_dataframe = pd.DataFrame(data = rates_matrix[index], index = currencies, columns = currencies)
    final_dataframe.to_csv(output_file, encoding='utf-8')