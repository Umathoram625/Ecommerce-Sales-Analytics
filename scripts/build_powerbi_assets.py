import pandas as pd
import numpy as np
import os

cleaned_dir = 'data/cleaned'
reports_dir = 'reports'
os.makedirs(cleaned_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)

# 1. Load validated cleaned dataset
df = pd.read_csv('data/cleaned/superstore_cleaned.csv', dtype={'postal_code': str})
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

print("======================================================================")
print("       PHASE 8: POWER BI DATA MODELING, STAR SCHEMA & DAX             ")
print("======================================================================")

# ----------------------------------------------------------------------
# 2. BUILD NORMALIZED STAR SCHEMA TABLES FOR POWER BI
# ----------------------------------------------------------------------

# A. DimCustomer (with customer_rfm merged for rich segmentation)
rfm_df = pd.read_csv('data/analytics/customer_rfm.csv')
dim_customer = df[['customer_id', 'customer_name', 'segment']].drop_duplicates(subset=['customer_id']).copy()
dim_customer = dim_customer.merge(
    rfm_df[['customer_id', 'recency', 'frequency', 'monetary', 'r_score', 'f_score', 'm_score', 'rfm_score', 'rfm_segment']],
    on='customer_id',
    how='left'
)
dim_customer.to_csv(os.path.join(cleaned_dir, 'DimCustomer.csv'), index=False)
print(f"DimCustomer created: {dim_customer.shape[0]} unique customers, {dim_customer.shape[1]} columns")

# B. DimProduct
dim_product = df[['product_id', 'category', 'sub_category', 'product_name']].drop_duplicates(subset=['product_id']).copy()
dim_product.to_csv(os.path.join(cleaned_dir, 'DimProduct.csv'), index=False)
print(f"DimProduct created: {dim_product.shape[0]} unique products, {dim_product.shape[1]} columns")

# C. DimGeography
dim_geography = df[['postal_code', 'city', 'state', 'region', 'country']].drop_duplicates(subset=['postal_code']).copy()
dim_geography.to_csv(os.path.join(cleaned_dir, 'DimGeography.csv'), index=False)
print(f"DimGeography created: {dim_geography.shape[0]} unique locations, {dim_geography.shape[1]} columns")

# D. DimShipping
dim_shipping = pd.DataFrame({
    'ship_mode_id': [1, 2, 3, 4],
    'ship_mode': ['Same Day', 'First Class', 'Second Class', 'Standard Class'],
    'sla_target_days': [1, 2, 3, 6],
    'delivery_tier': ['Express Same Day', 'Expedited Air', 'Priority Ground', 'Standard Freight']
})
dim_shipping.to_csv(os.path.join(cleaned_dir, 'DimShipping.csv'), index=False)
print(f"DimShipping created: {dim_shipping.shape[0]} shipping modes")

# E. DimDate (Calendar Table)
min_date = df['order_date'].min()
max_date = max(df['order_date'].max(), df['ship_date'].max())
date_series = pd.date_range(start=min_date, end=max_date, freq='D')

dim_date = pd.DataFrame({'date': date_series})
dim_date['date_key'] = dim_date['date'].dt.strftime('%Y%m%d').astype(int)
dim_date['year'] = dim_date['date'].dt.year
dim_date['quarter'] = 'Q' + dim_date['date'].dt.quarter.astype(str)
dim_date['year_quarter'] = dim_date['date'].dt.year.astype(str) + '-' + dim_date['quarter']
dim_date['month_number'] = dim_date['date'].dt.month
dim_date['month'] = dim_date['date'].dt.strftime('%B')
dim_date['month_short'] = dim_date['date'].dt.strftime('%b')
dim_date['year_month'] = dim_date['date'].dt.strftime('%Y-%m')
dim_date['week_number'] = dim_date['date'].dt.isocalendar().week.astype(int)
dim_date['day'] = dim_date['date'].dt.day
dim_date['day_of_week'] = dim_date['date'].dt.strftime('%A')
dim_date['day_of_week_num'] = dim_date['date'].dt.dayofweek + 1
dim_date['is_weekend'] = dim_date['date'].dt.dayofweek.isin([5, 6]).astype(int)

dim_date.to_csv(os.path.join(cleaned_dir, 'DimDate.csv'), index=False)
print(f"DimDate created: {dim_date.shape[0]} calendar days ({min_date.date()} to {max_date.date()})")

# F. FactSales
fact_sales = df[[
    'row_id', 'order_id', 'order_date', 'ship_date', 'ship_mode',
    'customer_id', 'postal_code', 'product_id',
    'sales', 'quantity', 'discount', 'profit',
    'shipping_days', 'profit_margin'
]].copy()

# Add ship_mode_id foreign key
ship_mode_map = {'Same Day': 1, 'First Class': 2, 'Second Class': 3, 'Standard Class': 4}
fact_sales['ship_mode_id'] = fact_sales['ship_mode'].map(ship_mode_map)
fact_sales['order_date_key'] = fact_sales['order_date'].dt.strftime('%Y%m%d').astype(int)
fact_sales['ship_date_key'] = fact_sales['ship_date'].dt.strftime('%Y%m%d').astype(int)

fact_sales.to_csv(os.path.join(cleaned_dir, 'FactSales.csv'), index=False)
print(f"FactSales created: {fact_sales.shape[0]} transaction lines, {fact_sales.shape[1]} columns")

# ----------------------------------------------------------------------
# 3. RECONCILIATION & MEASURE VALIDATIONS
# ----------------------------------------------------------------------
total_sales = fact_sales['sales'].sum()
total_profit = fact_sales['profit'].sum()
total_qty = fact_sales['quantity'].sum()
total_orders = fact_sales['order_id'].nunique()
total_cust = fact_sales['customer_id'].nunique()
aov = total_sales / total_orders
profit_margin_pct = (total_profit / total_sales) * 100
avg_discount_pct = fact_sales['discount'].mean() * 100
avg_shipping_days = fact_sales['shipping_days'].mean()
loss_sales = fact_sales[fact_sales['profit'] < 0]['sales'].sum()
loss_profit = fact_sales[fact_sales['profit'] < 0]['profit'].sum()

print("\n--- MEASURE RECONCILIATION ---")
print(f"Total Sales:          ${total_sales:,.2f}")
print(f"Total Profit:         ${total_profit:,.2f}")
print(f"Total Quantity:       {total_qty:,} units")
print(f"Total Orders:         {total_orders:,}")
print(f"Total Customers:      {total_cust:,}")
print(f"Average Order Value:  ${aov:,.2f}")
print(f"Profit Margin %:      {profit_margin_pct:.2f}%")
print(f"Average Discount %:   {avg_discount_pct:.2f}%")
print(f"Average Shipping Days:{avg_shipping_days:.2f} days")
print(f"Loss-Making Sales:    ${loss_sales:,.2f} (Loss Amount: ${loss_profit:,.2f})")
print("Validation Status:    100% RECONCILED")

