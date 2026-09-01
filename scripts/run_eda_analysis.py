import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# Setup aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

img_dir = 'dashboard_images'
os.makedirs(img_dir, exist_ok=True)

df = pd.read_csv('data/cleaned/superstore_cleaned.csv', dtype={'postal_code': str})
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

print('======================================================================')
print('           PHASE 5: EXPLORATORY DATA ANALYSIS COMPUTATIONS            ')
print('======================================================================')

# ----------------------------------------------------------------------
# 1. EXECUTIVE KPIs
# ----------------------------------------------------------------------
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
total_quantity = df['quantity'].sum()
total_orders = df['order_id'].nunique()
unique_customers = df['customer_id'].nunique()
aov = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100
avg_discount = df['discount'].mean() * 100
avg_shipping_days = df['shipping_days'].mean()

print("\n--- 1. EXECUTIVE KPIS ---")
print(f"Total Sales:            ${total_sales:,.2f}")
print(f"Total Profit:           ${total_profit:,.2f}")
print(f"Total Quantity Sold:    {total_quantity:,} units")
print(f"Total Unique Orders:    {total_orders:,}")
print(f"Average Order Value:    ${aov:,.2f}")
print(f"Overall Profit Margin:  {profit_margin:.2f}%")
print(f"Average Discount Rate:  {avg_discount:.2f}%")
print(f"Average Shipping Days:  {avg_shipping_days:.2f} days")

# ----------------------------------------------------------------------
# 2. TIME ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 2. TIME ANALYSIS ---")
# By Year
yearly = df.groupby('year').agg({
    'sales': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'order_id': 'nunique'
}).reset_index()
yearly['profit_margin'] = (yearly['profit'] / yearly['sales']) * 100
yearly['yoy_sales_growth'] = yearly['sales'].pct_change() * 100
yearly['yoy_profit_growth'] = yearly['profit'].pct_change() * 100
print("Yearly Performance:")
print(yearly.to_string(index=False))

# Monthly Trends
monthly = df.groupby('year_month').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()
monthly['profit_margin'] = (monthly['profit'] / monthly['sales']) * 100

# Top Months by Sales
top_months = monthly.sort_values('sales', ascending=False).head(5)
print("\nTop 5 Months by Sales:")
print(top_months.to_string(index=False))

# Seasonality by Month Number (Aggregated across all years)
monthly_seasonality = df.groupby('month_number').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()
monthly_seasonality['month_name'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print("\nAggregated Seasonality by Month:")
print(monthly_seasonality[['month_name', 'sales', 'profit', 'order_id']].to_string(index=False))

# Quarterly Performance
quarterly = df.groupby(['year', 'quarter']).agg({
    'sales': 'sum',
    'profit': 'sum'
}).reset_index()
print("\nQuarterly Performance Summary:")
print(quarterly.to_string(index=False))

# ----------------------------------------------------------------------
# 3. CATEGORY & SUB-CATEGORY ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 3. CATEGORY & SUB-CATEGORY ANALYSIS ---")
cat_summary = df.groupby('category').agg({
    'sales': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'order_id': 'nunique'
}).reset_index()
cat_summary['profit_margin'] = (cat_summary['profit'] / cat_summary['sales']) * 100
cat_summary['sales_share'] = (cat_summary['sales'] / total_sales) * 100
cat_summary['profit_share'] = (cat_summary['profit'] / total_profit) * 100
print("Category Breakdown:")
print(cat_summary.sort_values('sales', ascending=False).to_string(index=False))

subcat_summary = df.groupby(['category', 'sub_category']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'order_id': 'nunique'
}).reset_index()
subcat_summary['profit_margin'] = (subcat_summary['profit'] / subcat_summary['sales']) * 100
print("\nSub-Category Breakdown (Sorted by Profit):")
print(subcat_summary.sort_values('profit', ascending=False).to_string(index=False))

loss_subcats = subcat_summary[subcat_summary['profit'] < 0]
print("\nLoss-Making Sub-Categories:")
print(loss_subcats[['sub_category', 'category', 'sales', 'profit', 'profit_margin']].to_string(index=False))

# ----------------------------------------------------------------------
# 4. PRODUCT ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 4. PRODUCT ANALYSIS ---")
prod_summary = df.groupby(['product_id', 'product_name', 'category', 'sub_category']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'quantity': 'sum'
}).reset_index()
prod_summary['profit_margin'] = (prod_summary['profit'] / prod_summary['sales']) * 100

top10_prod_sales = prod_summary.sort_values('sales', ascending=False).head(10)
top10_prod_profit = prod_summary.sort_values('profit', ascending=False).head(10)
bottom10_prod_profit = prod_summary.sort_values('profit', ascending=True).head(10)

print("\nTop 5 Products by Sales:")
print(top10_prod_sales[['product_name', 'sales', 'profit', 'profit_margin']].head(5).to_string(index=False))

print("\nTop 5 Products by Profit:")
print(top10_prod_profit[['product_name', 'sales', 'profit', 'profit_margin']].head(5).to_string(index=False))

print("\nBottom 5 Products by Profit (Worst Loss Leaders):")
print(bottom10_prod_profit[['product_name', 'sales', 'profit', 'profit_margin']].head(5).to_string(index=False))

# High Sales (> $3,000) but Negative Profit
high_sales_neg_profit = prod_summary[(prod_summary['sales'] > 3000) & (prod_summary['profit'] < 0)]
print(f"\nProducts with High Sales (> $3,000) but Negative Profit ({len(high_sales_neg_profit)} products):")
print(high_sales_neg_profit[['product_name', 'sales', 'profit', 'profit_margin']].to_string(index=False))

# ----------------------------------------------------------------------
# 5. CUSTOMER ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 5. CUSTOMER ANALYSIS ---")
cust_summary = df.groupby(['customer_id', 'customer_name', 'segment']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique',
    'quantity': 'sum'
}).reset_index()
cust_summary['profit_margin'] = (cust_summary['profit'] / cust_summary['sales']) * 100

top10_cust_sales = cust_summary.sort_values('sales', ascending=False).head(10)
top10_cust_profit = cust_summary.sort_values('profit', ascending=False).head(10)

print(f"Total Unique Customers: {len(cust_summary)}")
print(f"Average Sales per Customer: ${cust_summary['sales'].mean():,.2f}")
print(f"Average Profit per Customer: ${cust_summary['profit'].mean():,.2f}")
top10_sales_contrib = (top10_cust_sales['sales'].sum() / total_sales) * 100
top20pct_count = int(len(cust_summary) * 0.20)
top20pct_sales = cust_summary.sort_values('sales', ascending=False).head(top20pct_count)['sales'].sum()
print(f"Top 10 Customers Revenue Contribution: {top10_sales_contrib:.2f}% (${top10_cust_sales['sales'].sum():,.2f})")
print(f"Top 20% Customers ({top20pct_count} customers) Contribution: {(top20pct_sales / total_sales) * 100:.2f}% (${top20pct_sales:,.2f})")

# ----------------------------------------------------------------------
# 6. SEGMENT ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 6. SEGMENT ANALYSIS ---")
seg_summary = df.groupby('segment').agg({
    'sales': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'order_id': 'nunique',
    'customer_id': 'nunique'
}).reset_index()
seg_summary['profit_margin'] = (seg_summary['profit'] / seg_summary['sales']) * 100
seg_summary['sales_share'] = (seg_summary['sales'] / total_sales) * 100
seg_summary['profit_share'] = (seg_summary['profit'] / total_profit) * 100
print(seg_summary.to_string(index=False))

# ----------------------------------------------------------------------
# 7. REGIONAL & STATE ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 7. REGIONAL & STATE ANALYSIS ---")
reg_summary = df.groupby('region').agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()
reg_summary['profit_margin'] = (reg_summary['profit'] / reg_summary['sales']) * 100
print("Regional Performance:")
print(reg_summary.sort_values('profit', ascending=False).to_string(index=False))

state_summary = df.groupby(['state', 'region']).agg({
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique',
    'discount': 'mean'
}).reset_index()
state_summary['profit_margin'] = (state_summary['profit'] / state_summary['sales']) * 100
state_summary['avg_discount_pct'] = state_summary['discount'] * 100

top5_states = state_summary.sort_values('profit', ascending=False).head(5)
bottom5_states = state_summary.sort_values('profit', ascending=True).head(5)
loss_states = state_summary[state_summary['profit'] < 0]

print(f"\nTop 5 Most Profitable States:")
print(top5_states[['state', 'region', 'sales', 'profit', 'profit_margin', 'avg_discount_pct']].to_string(index=False))

print(f"\nTotal Loss-Making States: {len(loss_states)} states")
print("Bottom 5 Loss-Making States:")
print(bottom5_states[['state', 'region', 'sales', 'profit', 'profit_margin', 'avg_discount_pct']].to_string(index=False))

# ----------------------------------------------------------------------
# 8. DISCOUNT & PROFITABILITY ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 8. DISCOUNT & PROFITABILITY ANALYSIS ---")
df['discount_pct_round'] = (df['discount'] * 100).round(0).astype(int)
discount_levels = df.groupby('discount_pct_round').agg({
    'sales': ['count', 'sum', 'mean'],
    'profit': ['sum', 'mean'],
    'profit_margin': 'mean'
})
print("Performance across exact discount percentages:")
disc_agg = df.groupby('discount').agg({
    'sales': ['count', 'sum'],
    'profit': ['sum', 'mean']
}).reset_index()
disc_agg.columns = ['discount', 'transaction_count', 'total_sales', 'total_profit', 'avg_profit_per_order']
disc_agg['profit_margin'] = (disc_agg['total_profit'] / disc_agg['total_sales']) * 100
print(disc_agg.to_string(index=False))

# Correlation
corr = df[['sales', 'quantity', 'discount', 'profit', 'shipping_days']].corr()
print("\nCorrelation Matrix:")
print(corr.to_string())

# ----------------------------------------------------------------------
# 9. SHIPPING ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 9. SHIPPING ANALYSIS ---")
ship_summary = df.groupby('ship_mode').agg({
    'shipping_days': ['mean', 'min', 'max'],
    'sales': 'sum',
    'profit': 'sum',
    'order_id': 'nunique'
}).reset_index()
ship_summary.columns = ['ship_mode', 'avg_shipping_days', 'min_shipping_days', 'max_shipping_days', 'total_sales', 'total_profit', 'order_count']
ship_summary['profit_margin'] = (ship_summary['total_profit'] / ship_summary['total_sales']) * 100
print(ship_summary.sort_values('avg_shipping_days').to_string(index=False))

# ----------------------------------------------------------------------
# 10. OUTLIER ANALYSIS
# ----------------------------------------------------------------------
print("\n--- 10. OUTLIER ANALYSIS ---")
def find_iqr_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = series[(series < lower) | (series > upper)]
    return len(outliers), lower, upper

for col in ['sales', 'quantity', 'discount', 'profit']:
    n_out, l, u = find_iqr_outliers(df[col])
    print(f"{col.capitalize()}: {n_out:,} outliers outside [{l:.2f}, {u:.2f}] (Min={df[col].min():.2f}, Max={df[col].max():.2f})")

print('All computations finished successfully.')
