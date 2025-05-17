import pandas as pd
import os

def clean_cpi_data():
    raw_data_dir = os.path.join('data', 'raw')
    cleaned_data_dir = os.path.join('data', 'cleaned')
    
    vn_cpi_path = os.path.join(raw_data_dir, 'vn_cpi.csv')
    vn_cpi_df = pd.read_csv(vn_cpi_path)
    
    jp_cpi_path = os.path.join(raw_data_dir, 'jp_cpi.csv')
    jp_cpi_df = pd.read_csv(jp_cpi_path)
    
    vn_cpi_df['date'] = pd.to_datetime(vn_cpi_df['Month/Year'], format='%m/%Y')
    vn_cpi_df = vn_cpi_df.sort_values('date')
    vn_cpi_df = vn_cpi_df.rename(columns={'CPI': 'vn_cpi'})
    
    jp_cpi_df['date'] = pd.to_datetime(jp_cpi_df['Month/Year'], format='%m/%Y')
    jp_cpi_df = jp_cpi_df.sort_values('date')
    jp_cpi_df = jp_cpi_df.rename(columns={'CPI': 'jp_cpi'})
    
    merged_df = pd.merge(vn_cpi_df[['date', 'vn_cpi']], jp_cpi_df[['date', 'jp_cpi']], on='date', how='outer')
    
    merged_df = merged_df.sort_values('date')
    
    output_path = os.path.join(cleaned_data_dir, 'cpi_data.csv')
    merged_df.to_csv(output_path, index=False)
    
if __name__ == "__main__":
    clean_cpi_data() 