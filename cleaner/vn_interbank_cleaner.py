import pandas as pd
import os

os.makedirs('data/cleaned', exist_ok=True)

input_path = 'data/raw/vn_interbank_interest.csv'
df = pd.read_csv(input_path)

df.columns = ['date', 'overnight_interest_rate']

def clean_rate(val):
    if pd.isna(val):
        return None
    val = str(val).replace(',', '.')
    val = val.strip('"')
    if val.startswith('.'):
        val = '0' + val
    try:
        return float(val)
    except:
        return None

df['overnight_interest_rate'] = df['overnight_interest_rate'].apply(clean_rate)

def clean_date(val):
    try:
        return pd.to_datetime(val, format='%d/%m/%Y')
    except:
        return pd.NaT

df['date'] = df['date'].apply(clean_date)

df = df.dropna(subset=['date', 'overnight_interest_rate'])

df = df.sort_values('date')

date_range = pd.date_range(df['date'].min(), df['date'].max(), freq='D')
full_df = pd.DataFrame({'date': date_range})

full_df = full_df.merge(df, on='date', how='left')

full_df['is_original'] = ~full_df['overnight_interest_rate'].isna()

full_df['overnight_interest_rate'] = full_df['overnight_interest_rate'].ffill()

output_path = 'data/cleaned/vn_interbank_interest_clean.csv'
full_df.to_csv(output_path, index=False)
