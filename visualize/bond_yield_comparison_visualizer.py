import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_bond_yield_comparison():
    vn_data_path = os.path.join('data', 'cleaned', 'vn_bond_yield_cleaned.csv')
    jp_data_path = os.path.join('data', 'cleaned', 'jp_bond_yield_cleaned.csv')
    
    vn_df = pd.read_csv(vn_data_path)
    jp_df = pd.read_csv(jp_data_path)
    
    vn_df['date'] = pd.to_datetime(vn_df['date'])
    jp_df['date'] = pd.to_datetime(jp_df['date'])
    
    output_dir = os.path.join('visualize', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(15, 7))
    plt.plot(vn_df['date'], vn_df['yield'], label='VN Bond Yield', color='blue', linewidth=2)
    plt.plot(jp_df['date'], jp_df['yield'], label='JP Bond Yield', color='red', linewidth=2)
    plt.title('VN vs JP Bond Yield Comparison Over Time')
    plt.xlabel('Date')
    plt.ylabel('Yield (%)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bond_yield_comparison_timeline.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    data = [vn_df['yield'], jp_df['yield']]
    plt.boxplot(data, tick_labels=['VN Bond Yield', 'JP Bond Yield'], patch_artist=True)
    plt.title('Boxplot Comparison of VN and JP Bond Yields')
    plt.ylabel('Yield (%)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bond_yield_comparison_boxplot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    vn_df['year'] = vn_df['date'].dt.year
    jp_df['year'] = jp_df['date'].dt.year
    
    vn_yearly = vn_df.groupby('year')['yield'].mean()
    jp_yearly = jp_df.groupby('year')['yield'].mean()
    
    plt.figure(figsize=(12, 6))
    years = sorted(set(vn_yearly.index) | set(jp_yearly.index))
    x = range(len(years))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], vn_yearly, width, label='VN Bond Yield', color='blue', alpha=0.7)
    plt.bar([i + width/2 for i in x], jp_yearly, width, label='JP Bond Yield', color='red', alpha=0.7)
    
    plt.title('Average Bond Yield by Year: VN vs JP')
    plt.xlabel('Year')
    plt.ylabel('Average Yield (%)')
    plt.xticks(x, years, rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bond_yield_comparison_yearly.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    vn_df['month'] = vn_df['date'].dt.month
    jp_df['month'] = jp_df['date'].dt.month
    
    vn_monthly = vn_df.groupby('month')['yield'].mean()
    jp_monthly = jp_df.groupby('month')['yield'].mean()
    
    plt.figure(figsize=(12, 6))
    months = range(1, 13)
    x = range(len(months))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], vn_monthly, width, label='VN Bond Yield', color='blue', alpha=0.7)
    plt.bar([i + width/2 for i in x], jp_monthly, width, label='JP Bond Yield', color='red', alpha=0.7)
    
    plt.title('Average Bond Yield by Month (All Years): VN vs JP')
    plt.xlabel('Month')
    plt.ylabel('Average Yield (%)')
    plt.xticks(x, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bond_yield_comparison_monthly.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, ax1 = plt.subplots(figsize=(15, 7))
    color_vn = 'blue'
    color_jp = 'red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('VN Bond Yield (%)', color=color_vn)
    l1, = ax1.plot(vn_df['date'], vn_df['yield'], color=color_vn, label='VN Bond Yield', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color_vn)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('JP Bond Yield (%)', color=color_jp)
    l2, = ax2.plot(jp_df['date'], jp_df['yield'], color=color_jp, label='JP Bond Yield', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color_jp)
    
    plt.title('VN vs JP Bond Yield Comparison (Twin Y-Axis)')
    fig.tight_layout()
    lines = [l1, l2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper left')
    plt.savefig(os.path.join(output_dir, 'bond_yield_comparison_twin_axis.png'), dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    visualize_bond_yield_comparison() 