import pandas as pd

pollutants = ['PM2.5_24h', 'PM10_24h', 'SO2', 'NO2', 'O3', 'CO']

quarter_files = [f"../data/data_Q{i}.xlsx" for i in range(1, 5)]

cities = ['南京', '上海', '杭州']

quarterly_means = []

for i, file in enumerate(quarter_files, start=1):
    df = pd.read_excel(file)
    df = df[df['city'].isin(cities)]
    mean_df = df.groupby('city')[pollutants].mean()
    mean_df['季度'] = f'Q{i}'
    quarterly_means.append(mean_df.reset_index())


result = pd.concat(quarterly_means, axis=0)

result.to_excel("../data/city3_quarterly_avg.xlsx", index=False)

