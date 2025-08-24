import pandas as pd

df = pd.read_excel('../data/data_all.xlsx')

df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

df['quarter'] = df['date'].dt.quarter

for q in range(1, 5):
    q_df = df[df['quarter'] == q].copy()
    q_df['date'] = q_df['date'].dt.strftime('%Y-%m-%d')
    q_df.to_excel(f'../data/data_Q{q}.xlsx', index=False)
