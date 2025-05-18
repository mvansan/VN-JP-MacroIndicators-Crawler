import pandas as pd
import numpy as np
from datetime import datetime

def clean_vn_bond():
    df = pd.read_csv('data/raw/vn_bond_yield.csv')
    
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    
    df['yield'] = df['yield'].str.rstrip('%').astype('float')
    
    df = df.sort_values('date')
    
    start_date = pd.Timestamp('2020-01-01')
    end_date = df['date'].max()
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    complete_df = pd.DataFrame({'date': date_range})
    
    complete_df = complete_df.merge(df, on='date', how='left')
    
    complete_df['yield'] = complete_df['yield'].ffill().bfill()
    
    complete_df.to_csv('data/cleaned/vn_bond_yield_cleaned.csv', index=False)
    
if __name__ == "__main__":
    clean_vn_bond() 