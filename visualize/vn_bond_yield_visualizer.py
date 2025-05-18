import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_vn_bond():
    data_path = os.path.join('data', 'cleaned', 'vn_bond_yield_cleaned.csv')
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    output_dir = os.path.join('visualize', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['yield'], label='VN Bond Yield', color='blue', linewidth=2)
    plt.title('VN Bond Yield Over Time')
    plt.xlabel('Date')
    plt.ylabel('Yield (%)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'vn_bond_yield_timeline.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(10, 4))
    plt.boxplot(df['yield'], vert=False, patch_artist=True, showfliers=True)
    plt.title('Boxplot of VN Bond Yield')
    plt.xlabel('Yield (%)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'vn_bond_yield_boxplot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    df['year'] = df['date'].dt.year
    plt.figure(figsize=(14, 6))
    df.boxplot(column='yield', by='year', vert=False, grid=True, showfliers=True, patch_artist=True)
    plt.title('Boxplot of VN Bond Yield by Year')
    plt.suptitle('')
    plt.xlabel('Yield (%)')
    plt.ylabel('Year')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'vn_bond_yield_by_year.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    df['month'] = df['date'].dt.month
    plt.figure(figsize=(14, 6))
    df.boxplot(column='yield', by='month', vert=False, grid=True, showfliers=True, patch_artist=True)
    plt.title('Boxplot of VN Bond Yield by Month (All Years)')
    plt.suptitle('')
    plt.xlabel('Yield (%)')
    plt.ylabel('Month')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'vn_bond_yield_by_month.png'), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    visualize_vn_bond() 