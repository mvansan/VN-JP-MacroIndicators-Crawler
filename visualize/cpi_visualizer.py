import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_cpi_data():
    data_path = os.path.join('data', 'cleaned', 'cpi_data.csv')
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    output_dir = os.path.join('visualize', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['vn_cpi'], label='Vietnam CPI', color='blue', linewidth=2)
    plt.title('Vietnam CPI Over Time')
    plt.xlabel('Date')
    plt.ylabel('CPI Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'vn_cpi.png'))
    plt.close()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['jp_cpi'], label='Japan CPI', color='red', linewidth=2)
    plt.title('Japan CPI Over Time')
    plt.xlabel('Date')
    plt.ylabel('CPI Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'jp_cpi.png'))
    plt.close()
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['vn_cpi'], label='Vietnam CPI', color='blue', linewidth=2)
    plt.plot(df['date'], df['jp_cpi'], label='Japan CPI', color='red', linewidth=2)
    plt.title('Vietnam vs Japan CPI Comparison')
    plt.xlabel('Date')
    plt.ylabel('CPI Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cpi_comparison.png'))
    plt.close()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[['vn_cpi', 'jp_cpi']].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation between Vietnam and Japan CPI')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cpi_correlation.png'))
    plt.close()
    
if __name__ == "__main__":
    visualize_cpi_data() 