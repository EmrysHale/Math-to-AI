import pandas as pd

df = pd.read_csv(
    '../data/data_03_cleaned_samples.csv',
    dtype=str
)

types = ['PM2.5_24h','PM10_24h','SO2','NO2','O3','CO','AQI']
cities = [c for c in df.columns if c not in ('date','hour','type')]

melted = df.melt(
    id_vars=['date','hour','type'],
    value_vars=cities,
    var_name='city',
    value_name='value'
)

melted['value'] = pd.to_numeric(melted['value'], errors='coerce')
wide = melted.pivot(index=['city','date','hour'], columns='type', values='value')

cols = ['city', 'date', 'hour'] + [t for t in types if t in wide.columns]
wide.reset_index()[cols] \
    .sort_values(by=['date', 'hour']) \
    .to_excel('../data/data_all.xlsx', index=False)