import pandas as pd
import os
import glob

INPUT_DIRS = ['../rawdata/rawdata_2023', '../rawdata/rawdata_2024', '../rawdata/rawdata_2025']
MAPPING_XLSX = '../data/station_code_mapping.xlsx'
YEARS = ['2023', '2024', '2025']

JS_CITIES = ["南京","苏州","无锡","常州","镇江","扬州","泰州","南通","宿迁","盐城","连云港"]
ZJ_CITIES = ["杭州","宁波","温州","绍兴","嘉兴","湖州","金华","衢州","舟山","丽水","台州"]
SH_CITIES = ["上海"]
KEEP_TYPES = ['PM2.5_24h', 'PM10_24h', 'SO2', 'NO2', 'O3', 'CO', 'AQI']

def process_df(df, mapping, js_cities, zj_cities, sh_cities):
    targets = set(js_cities + zj_cities + sh_cities)
    map_jszh = mapping[mapping['城市'].isin(targets)]
    ids = map_jszh['监测点编码'].tolist()
    base_cols = ['date', 'hour', 'type']
    df = df[[c for c in df.columns if c in base_cols or c in ids]]

    id2city = map_jszh.set_index('监测点编码')['城市'].to_dict()
    df.columns = [id2city.get(c, c) for c in df.columns]
    df = df.dropna(axis=1, how='all')

    fixed = base_cols
    others = [c for c in df.columns if c not in fixed]
    counts = {}
    new_cols = []
    for col in others:
        counts[col] = counts.get(col, 0) + 1
        new_cols.append(f"{col}{counts[col]}")
    df.columns = fixed + new_cols
    return df

def merge_all_years(input_dirs, mapping_xlsx, years, keep_types, output_file):
    mapping = pd.read_excel(mapping_xlsx, dtype=str)
    all_frames = []

    for i in range(len(input_dirs)):
        input_dir = input_dirs[i]
        year = years[i]
        pattern = f"china_sites_{year}*.csv"
        files = sorted(glob.glob(os.path.join(input_dir, pattern)))

        for file in files:
            print(f"Processing {file}")
            df = pd.read_csv(file, dtype=str)
            processed = process_df(df, mapping, JS_CITIES, ZJ_CITIES, SH_CITIES)
            all_frames.append(processed)

    merged = pd.concat(all_frames, ignore_index=True)
    merged_filtered = merged[merged['type'].isin(keep_types)]
    merged_filtered.to_csv(output_file, index=False, encoding='utf-8')


merge_all_years(INPUT_DIRS, MAPPING_XLSX, YEARS, KEEP_TYPES, '../data/data_01_merged_all.csv')
