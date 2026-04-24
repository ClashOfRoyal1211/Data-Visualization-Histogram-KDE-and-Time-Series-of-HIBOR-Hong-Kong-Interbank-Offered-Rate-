import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load data from both sources
df_csv = pd.read_csv('Process CSV data/hibor_processed.csv')
df_json = pd.read_csv('hkd_rates.csv')

# Process dates for CSV data (quarterly)
df_csv['Date'] = df_csv['Date'].str.replace('-Q1', '-01-01').str.replace('-Q2', '-04-01').str.replace('-Q3', '-07-01').str.replace('-Q4', '-10-01')
df_csv['Date'] = pd.to_datetime(df_csv['Date'])
df_csv = df_csv.rename(columns={'ThreeMonthRate %': 'Rate'})
df_csv['Source'] = 'CSV (Quarterly)'

# Process dates for JSON data
def parse_period(p):
    p_str = str(p)
    if len(p_str) == 4:  # Annual
        return f"{p_str}-01-01"
    elif len(p_str) == 6:  # Monthly
        return f"{p_str[:4]}-{p_str[4:]}-01"
    else:
        return None

df_json['Date'] = df_json['Period'].apply(parse_period)
df_json['Date'] = pd.to_datetime(df_json['Date'], errors='coerce')
df_json = df_json.dropna(subset=['Date'])
df_json['Source'] = 'JSON (Detailed)'

# Combine datasets
df_combined = pd.concat([df_csv[['Date', 'Rate', 'Source']], df_json[['Date', 'Rate', 'Source']]], ignore_index=True)
df_combined = df_combined.sort_values('Date')

# Create a figure with subplots: timeline on left, distribution on right
fig, (ax_main, ax_dist) = plt.subplots(1, 2, figsize=(18, 7), gridspec_kw={'width_ratios': [2, 1]})
sns.set_theme(style="whitegrid")

# Add main title at the top
fig.suptitle("Statistical Distribution and Time-Series Analysis of 3-Month HIBOR (1996–2026)", fontsize=16, fontweight='bold', y=0.98)

# LEFT PLOT: Timeline
for source, color in [('CSV (Quarterly)', '#1f77b4'), ('JSON (Detailed)', '#ff7f0e')]:
    data = df_combined[df_combined['Source'] == source]
    ax_main.plot(data['Date'], data['Rate'], marker='o', linewidth=2, label=source, color=color)

# Set x-axis ticks by year
years = pd.date_range(start='1996-01-01', end='2026-01-01', freq='YS')
ax_main.set_xticks(years)
ax_main.set_xticklabels([d.strftime('%Y') for d in years], rotation=45)

ax_main.set_xlabel("Date (by Year)")
ax_main.set_ylabel("3-Month Interest Rate (%)")
ax_main.set_title("HKD Interest Rate Timeline", fontsize=12)
ax_main.legend(title='Data Source', loc='best')
ax_main.grid(True, alpha=0.3)

# RIGHT PLOT: Distribution (Histogram + KDE with own x and y axes)
from scipy import stats
rate_min, rate_max = df_combined['Rate'].min(), df_combined['Rate'].max()
rate_range = np.linspace(rate_min, rate_max, 100)
kde = stats.gaussian_kde(df_combined['Rate'])
kde_values = kde(rate_range)

# Plot histogram (vertical bars)
counts, bins = np.histogram(df_combined['Rate'], bins=20)
bin_centers = (bins[:-1] + bins[1:]) / 2
ax_dist.bar(bin_centers, counts, width=(bins[1]-bins[0]), alpha=0.6, color='steelblue', edgecolor='black', label='Histogram')

# Plot KDE on secondary y-axis
ax_dist_kde = ax_dist.twinx()
ax_dist_kde.plot(rate_range, kde_values, 'r-', linewidth=3, label='KDE')

ax_dist.set_xlabel("3-Month Interest Rate (%)")
ax_dist.set_ylabel("Frequency", color='steelblue')
ax_dist.tick_params(axis='y', labelcolor='steelblue')
ax_dist_kde.set_ylabel("Density", color='red')
ax_dist_kde.tick_params(axis='y', labelcolor='red')
ax_dist.set_title("Rate Distribution", fontsize=12)

# Combine legends
lines1, labels1 = ax_dist.get_legend_handles_labels()
lines2, labels2 = ax_dist_kde.get_legend_handles_labels()
ax_dist.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

plt.tight_layout()

# Save the plot
plt.savefig('combined_rates_plot_sources.png', bbox_inches='tight', dpi=150)

print("Plot with separate timeline and distribution axes saved as combined_rates_plot_sources.png")