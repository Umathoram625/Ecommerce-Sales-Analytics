import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

img_dir = 'dashboard_images'
os.makedirs(img_dir, exist_ok=True)

df = pd.read_csv('data/cleaned/superstore_cleaned.csv', dtype={'postal_code': str})
df['order_date'] = pd.to_datetime(df['order_date'])

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# 1. Monthly Sales & Profit Line Chart
monthly = df.groupby('year_month').agg({'sales': 'sum', 'profit': 'sum'}).reset_index()
fig, ax1 = plt.subplots(figsize=(13, 5))

color = '#1f77b4'
ax1.set_xlabel('Year-Month (2014-01 to 2017-12)', fontsize=11, fontweight='bold', labelpad=10)
ax1.set_ylabel('Total Sales ($)', color=color, fontsize=11, fontweight='bold')
line1 = ax1.plot(monthly['year_month'], monthly['sales'], color=color, marker='o', linewidth=2, label='Monthly Sales ($)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()  
color = '#2ca02c'
ax2.set_ylabel('Total Profit ($)', color=color, fontsize=11, fontweight='bold')
line2 = ax2.plot(monthly['year_month'], monthly['profit'], color=color, marker='s', linewidth=2, linestyle='--', label='Monthly Profit ($)')
ax2.tick_params(axis='y', labelcolor=color)
ax2.grid(False)

# Combined legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True)

plt.title('Monthly Sales and Profit Performance (2014 - 2017)', fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '01_monthly_sales_profit_trend.png'), dpi=300)
plt.close()

# 2. Category Sales & Profit Bar Chart
cat_df = df.groupby('category').agg({'sales': 'sum', 'profit': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(cat_df))
width = 0.35

rects1 = ax.bar(x - width/2, cat_df['sales'], width, label='Sales ($)', color='#1F4E79')
rects2 = ax.bar(x + width/2, cat_df['profit'], width, label='Profit ($)', color='#2CA02C')

ax.set_ylabel('Total USD ($)', fontweight='bold')
ax.set_title('Sales and Net Profit by Product Category', fontsize=13, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(cat_df['category'], fontsize=11, fontweight='bold')
ax.legend()

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'${h/1e3:.1f}k', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'${h/1e3:.1f}k', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(img_dir, '02_category_performance.png'), dpi=300)
plt.close()

# 3. Sub-Category Profitability Chart
subcat_df = df.groupby('sub_category').agg({'sales': 'sum', 'profit': 'sum'}).sort_values('profit', ascending=True).reset_index()
colors = ['#D62728' if p < 0 else '#2B8CBE' for p in subcat_df['profit']]

plt.figure(figsize=(10, 7))
bars = plt.barh(subcat_df['sub_category'], subcat_df['profit'], color=colors, height=0.65)
plt.axvline(0, color='black', linewidth=1, linestyle='--')
plt.title('Sub-Category Profitability (Identifying Loss Leaders)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Net Profit ($)', fontweight='bold')
plt.ylabel('Sub-Category', fontweight='bold')

for bar in bars:
    w = bar.get_width()
    ha = 'right' if w < 0 else 'left'
    offset = -600 if w < 0 else 600
    plt.annotate(f'${w:,.0f}', xy=(w, bar.get_y() + bar.get_height()/2),
                 xytext=(offset, 0), textcoords="offset points", ha=ha, va='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(img_dir, '03_subcategory_profitability.png'), dpi=300)
plt.close()

# 4. Regional Performance Bar Chart
reg_df = df.groupby('region').agg({'sales': 'sum', 'profit': 'sum'}).sort_values('sales', ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(reg_df))

rects1 = ax.bar(x - width/2, reg_df['sales'], width, label='Sales ($)', color='#3182BD')
rects2 = ax.bar(x + width/2, reg_df['profit'], width, label='Profit ($)', color='#31A354')
ax.set_title('Regional Sales and Profit Comparison', fontsize=13, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(reg_df['region'], fontsize=11, fontweight='bold')
ax.set_ylabel('Total USD ($)', fontweight='bold')
ax.legend()

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'${h/1e3:.1f}k', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'${h/1e3:.1f}k', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(img_dir, '04_regional_performance.png'), dpi=300)
plt.close()

# 5. Discount vs Profit Margin Analysis
disc_df = df.groupby('discount').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).reset_index()
disc_df['profit_margin'] = (disc_df['profit'] / disc_df['sales']) * 100

plt.figure(figsize=(9, 5))
colors = ['#2CA02C' if m >= 0 else '#D62728' for m in disc_df['profit_margin']]
bars = plt.bar(disc_df['discount'].astype(str), disc_df['profit_margin'], color=colors, width=0.5)
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.title('Profit Margin (%) Across Exact Discount Levels', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Discount Rate', fontweight='bold')
plt.ylabel('Profit Margin (%)', fontweight='bold')

for bar in bars:
    h = bar.get_height()
    va = 'bottom' if h >= 0 else 'top'
    plt.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                 xytext=(0, 3 if h >= 0 else -10), textcoords="offset points", ha='center', va=va, fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(img_dir, '05_discount_impact_on_margins.png'), dpi=300)
plt.close()

# 6. Top 10 Products by Revenue
top10_p = df.groupby('product_name').agg({'sales': 'sum'}).sort_values('sales', ascending=True).tail(10).reset_index()
plt.figure(figsize=(10, 6))
plt.barh(top10_p['product_name'], top10_p['sales'], color='#1F4E79', height=0.6)
plt.title('Top 10 Products by Total Revenue', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Revenue ($)', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '06_top10_products_sales.png'), dpi=300)
plt.close()

# 7. Top 10 Customers by Revenue
top10_c = df.groupby('customer_name').agg({'sales': 'sum'}).sort_values('sales', ascending=True).tail(10).reset_index()
plt.figure(figsize=(9, 5))
plt.barh(top10_c['customer_name'], top10_c['sales'], color='#4575B4', height=0.6)
plt.title('Top 10 Customers by Total Spend', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Lifetime Spend ($)', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '07_top10_customers.png'), dpi=300)
plt.close()

# 8. State-Level Profitability (Top 5 vs Bottom 5)
state_perf = df.groupby('state').agg({'profit': 'sum'}).reset_index()
top5_s = state_perf.sort_values('profit', ascending=False).head(5)
bottom5_s = state_perf.sort_values('profit', ascending=True).head(5)
state_comp = pd.concat([bottom5_s, top5_s]).sort_values('profit', ascending=True)

plt.figure(figsize=(9, 5))
colors = ['#D62728' if p < 0 else '#2CA02C' for p in state_comp['profit']]
bars = plt.barh(state_comp['state'], state_comp['profit'], color=colors, height=0.6)
plt.axvline(0, color='black', linewidth=1, linestyle='--')
plt.title('State Profitability: Top 5 Profitable vs Bottom 5 Loss-Making States', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Net Profit ($)', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, '08_state_profitability_comparison.png'), dpi=300)
plt.close()

print('All 8 EDA charts successfully rendered and saved.')
