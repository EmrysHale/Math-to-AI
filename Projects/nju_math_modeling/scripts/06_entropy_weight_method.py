import pandas as pd
import numpy as np

def transform(filename):
    df = pd.read_excel(filename)

    pollutant_columns = ['PM2.5_24h', 'PM10_24h', 'SO2', 'NO2', 'O3', 'CO']
    pollutant_data = df[pollutant_columns]

    return pollutant_data.dropna().to_numpy()


def entropy_weight(data):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)

    ranges = max_vals - min_vals
    ranges[ranges == 0] = 1e-12
    norm_data = (data-min_vals) / ranges

    eps = 1e-12
    col_sums = np.sum(norm_data, axis=0)

    col_sums[col_sums == 0] = eps
    P = norm_data / col_sums
    P = np.clip(P, eps, 1)

    n = data.shape[0]
    k = 1 / np.log(n)
    entropy = -k * np.sum(P * np.log(P), axis=0)

    d = 1 - entropy

    if np.sum(d) == 0:
        weights = np.full_like(d, 1 / len(d))
    else:
        weights = d / np.sum(d)

    return weights

file_lst=[f"../data/data_Q{i}.xlsx" for i in range(1,5)]
weight_lst=[]

for i in range(0,4):
    weight_lst.append(entropy_weight(transform(file_lst[i])))
    print(weight_lst[i])





