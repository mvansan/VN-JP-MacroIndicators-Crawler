import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

input_path = 'data/cleaned/vn_interbank_interest_clean.csv'
df = pd.read_csv(input_path, parse_dates=['date'])

os.makedirs('visualize/images', exist_ok=True)

def detect_outliers_zscore(series, threshold=3):
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / std
    return np.abs(z_scores) > threshold

df['is_outlier'] = detect_outliers_zscore(df['overnight_interest_rate'])

plt.figure(figsize=(16,6))

orig = df[(df['is_original']) & (~df['is_outlier'])]
plt.plot(orig['date'], orig['overnight_interest_rate'], 'o-', label='Original', markersize=4, color='blue')

filled = df[(~df['is_original']) & (~df['is_outlier'])]
plt.plot(filled['date'], filled['overnight_interest_rate'], '.', label='Filled', markersize=2, color='orange')

outliers = df[df['is_outlier']]
plt.plot(outliers['date'], outliers['overnight_interest_rate'], 'ro', label='Outlier', markersize=7, fillstyle='none')

plt.title('Vietnam Interbank Overnight Interest Rate (Cleaned, Outliers Highlighted)')
plt.xlabel('Date')
plt.ylabel('Overnight Interest Rate (%)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('visualize/images/vn_interbank_interest_rate_timeline.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

plt.figure(figsize=(10, 4))
box = plt.boxplot(df['overnight_interest_rate'], vert=False, patch_artist=True, showfliers=True)
plt.title('Boxplot of Vietnam Interbank Overnight Interest Rate (All Data)')
plt.xlabel('Overnight Interest Rate (%)')
plt.tight_layout()

q1 = df['overnight_interest_rate'].quantile(0.25)
q3 = df['overnight_interest_rate'].quantile(0.75)
median = df['overnight_interest_rate'].median()
min_val = df['overnight_interest_rate'].min()
max_val = df['overnight_interest_rate'].max()
outlier_val = outliers['overnight_interest_rate'].values[0] if not outliers.empty else median

plt.annotate('Median (Trung vị)', xy=(median, 1), xytext=(median+1, 1.1),
             arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=10, color='black')
plt.annotate('Box: 25%-75% (Q1-Q3)', xy=(q1, 1), xytext=(q1+1, 1.15),
             arrowprops=dict(facecolor='blue', arrowstyle='->'), fontsize=10, color='blue')
plt.annotate('Box: 25%-75% (Q1-Q3)', xy=(q3, 1), xytext=(q3+1, 1.15),
             arrowprops=dict(facecolor='blue', arrowstyle='->'), fontsize=10, color='blue')
plt.annotate('Whiskers: min/max trong phạm vi thường', xy=(min_val, 1), xytext=(min_val+1, 0.95),
             arrowprops=dict(facecolor='green', arrowstyle='->'), fontsize=10, color='green')
plt.annotate('Whiskers: min/max trong phạm vi thường', xy=(max_val, 1), xytext=(max_val-1, 0.95),
             arrowprops=dict(facecolor='green', arrowstyle='->'), fontsize=10, color='green')
plt.annotate('Outlier', xy=(outlier_val, 1), xytext=(outlier_val+1, 0.85),
             arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=10, color='red')
plt.savefig('visualize/images/vn_interbank_interest_rate_boxplot.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

df['year'] = df['date'].dt.year
plt.figure(figsize=(14, 6))
df.boxplot(column='overnight_interest_rate', by='year', vert=False, grid=True, showfliers=True, patch_artist=True)
plt.title('Boxplot of Overnight Interest Rate by Year')
plt.suptitle('')
plt.xlabel('Overnight Interest Rate (%)')
plt.ylabel('Year')
plt.tight_layout()
plt.savefig('visualize/images/vn_interbank_interest_rate_by_year.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

df['month'] = df['date'].dt.month
plt.figure(figsize=(14, 6))
df.boxplot(column='overnight_interest_rate', by='month', vert=False, grid=True, showfliers=True, patch_artist=True)
plt.title('Boxplot of Overnight Interest Rate by Month (All Years)')
plt.suptitle('')
plt.xlabel('Overnight Interest Rate (%)')
plt.ylabel('Month')
plt.tight_layout()
plt.savefig('visualize/images/vn_interbank_interest_rate_by_month.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close() 