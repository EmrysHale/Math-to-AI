import pandas as pd
import re
from collections import defaultdict

input_path = '../data/data_01_merged_all.csv'
df = pd.read_csv(input_path, dtype=str)

meas_cols = df.columns.difference(['date','hour','type'])
df_num = df[meas_cols].apply(pd.to_numeric, errors='coerce')

city_prefix = [re.match(r'(.+?)(\d+)$', c).group(1) for c in meas_cols]

city_cols = defaultdict(list)
for col, city in zip(meas_cols, city_prefix):
    city_cols[city].append(col)

avg_df = pd.DataFrame({
    city: df_num[cols].mean(axis=1, skipna=True).round(1)
    for city, cols in city_cols.items()
})

out = pd.concat([df[['date','hour','type']].reset_index(drop=True), avg_df], axis=1)

output_path = '../data/data_02_avg_by_city.csv'
out.to_csv(output_path, index=False, encoding='utf-8')

