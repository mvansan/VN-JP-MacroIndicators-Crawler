import pandas as pd
import numpy as np
from datetime import datetime

def clean_jp_bond():
    df = pd.read_csv('data/raw/jp_bond_yield.csv')
    
    df['date'] = pd.to_datetime(df['date'], format='%b %d, %Y')
    
    df['yield'] = df['yield'].str.rstrip('%').astype('float')
    
    date_range = pd.date_range(start='2020-01-01', end=df['date'].max(), freq='D')
    complete_df = pd.DataFrame({'date': date_range})
    
    df = pd.merge(complete_df, df, on='date', how='left')
    
    df = df.sort_values('date')
    
    df['yield'] = df['yield'].ffill().bfill()
    
    df.to_csv('data/cleaned/jp_bond_yield_cleaned.csv', index=False)
    
if __name__ == "__main__":
    clean_jp_bond() 