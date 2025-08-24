import pandas as pd

df = pd.read_csv(
    '../data/data_02_avg_by_city.csv',
    dtype=str
)

meas_cols = [c for c in df.columns if c not in ('date', 'hour', 'type')]

row_has_na = df[meas_cols].isna().any(axis=1)

bad_hours = set(zip(df.loc[row_has_na, 'date'], df.loc[row_has_na, 'hour']))

df_clean = df.loc[~df.apply(lambda r: (r['date'], r['hour']) in bad_hours, axis=1)]

df_clean.to_csv(
    '../data/data_03_cleaned_samples.csv',
    index=False,
    encoding='utf-8'
)
