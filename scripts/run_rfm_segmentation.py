import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# Aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

rfm_img_dir = 'dashboard_images/rfm'
analytics_dir = 'data/analytics'
reports_dir = 'reports'
notebooks_dir = 'notebooks'

os.makedirs(rfm_img_dir, exist_ok=True)
os.makedirs(analytics_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)
os.makedirs(notebooks_dir, exist_ok=True)

# 1. Load validated dataset
df = pd.read_csv('data/cleaned/superstore_cleaned.csv', dtype={'postal_code': str})
df['order_date'] = pd.to_datetime(df['order_date'])

total_sales_dataset = df['sales'].sum()
total_profit_dataset = df['profit'].sum()
total_unique_customers = df['customer_id'].nunique()
reference_date = df['order_date'].max()

print("======================================================================")
print("            PHASE 7: CUSTOMER BEHAVIOR & RFM SEGMENTATION             ")
print("======================================================================")
print(f"Dataset Reference Date (Max Order Date): {reference_date.strftime('%Y-%m-%d')}")
print(f"Total Unique Customers: {total_unique_customers}")
print(f"Dataset Total Sales:   ${total_sales_dataset:,.2f}")
print(f"Dataset Total Profit:  ${total_profit_dataset:,.2f}")

# 2. Compute Customer Base & RFM Metrics
rfm = df.groupby(['customer_id', 'customer_name', 'segment']).agg(
    recency=('order_date', lambda x: (reference_date - x.max()).days),
    frequency=('order_id', 'nunique'),
    monetary=('sales', 'sum'),
    total_profit=('profit', 'sum'),
    total_quantity=('quantity', 'sum'),
    first_order_date=('order_date', 'min'),
    last_order_date=('order_date', 'max')
).reset_index()

rfm['aov'] = (rfm['monetary'] / rfm['frequency']).round(2)
rfm['profit_margin_pct'] = ((rfm['total_profit'] / rfm['monetary']) * 100).round(2)

# 3. RFM Scoring Methodology (Quantile / Rank-based 1 to 5)
# Recency: Lower days = Higher Score (5 is most recent)
rfm['r_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1]).astype(int)

# Frequency: Higher frequency = Higher Score (handle tied ranks using rank(method='first'))
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

# Monetary: Higher spend = Higher Score (5 is highest spend)
rfm['m_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5]).astype(int)

rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
rfm['rfm_combined_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

# 4. RFM Segmentation Framework Logic
def assign_segment(row):
    r, f, m = row['r_score'], row['f_score'], row['m_score']
    
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2 and m >= 2:
        return 'Potential Loyalists'
    elif r >= 4 and f == 1 and m == 1:
        return 'New Customers'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r >= 3 and f <= 2 and m <= 2:
        return 'Need Attention'
    elif r <= 2 and f <= 2 and m >= 3:
        return 'About to Sleep'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost Customers'
    else:
        return 'Hibernating'

rfm['rfm_segment'] = rfm.apply(assign_segment, axis=1)

# 5. Export Customer RFM Dataset
output_rfm_path = os.path.join(analytics_dir, 'customer_rfm.csv')
rfm.to_csv(output_rfm_path, index=False)
print(f"Customer RFM dataset exported to {output_rfm_path} ({len(rfm)} records)")

# 6. Segment Summary & Analysis
seg_summary = rfm.groupby('rfm_segment').agg(
    customer_count=('customer_id', 'count'),
    total_sales=('monetary', 'sum'),
    total_profit=('total_profit', 'sum'),
    avg_sales=('monetary', 'mean'),
    avg_profit=('total_profit', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_recency=('recency', 'mean')
).reset_index()

seg_summary['pct_customers'] = (seg_summary['customer_count'] / len(rfm)) * 100
seg_summary['pct_sales'] = (seg_summary['total_sales'] / total_sales_dataset) * 100
seg_summary['pct_profit'] = (seg_summary['total_profit'] / total_profit_dataset) * 100
seg_summary['profit_margin_pct'] = (seg_summary['total_profit'] / seg_summary['total_sales']) * 100

seg_summary = seg_summary.sort_values('total_sales', ascending=False).reset_index(drop=True)

print("\n--- RFM SEGMENT PERFORMANCE SUMMARY ---")
print(seg_summary[['rfm_segment', 'customer_count', 'pct_customers', 'total_sales', 'pct_sales', 'total_profit', 'pct_profit', 'profit_margin_pct']].to_string(index=False))

# 7. Customer Value Highlights
top10_sales = rfm.sort_values('monetary', ascending=False).head(10)
top10_profit = rfm.sort_values('total_profit', ascending=False).head(10)
top10_freq = rfm.sort_values('frequency', ascending=False).head(10)
high_sales_neg_profit = rfm[(rfm['monetary'] > 5000) & (rfm['total_profit'] < 0)]
at_risk_customers = rfm[rfm['rfm_segment'] == 'At Risk']

print(f"\n--- Customer Value Highlights ---")
print(f"Top Spender: {top10_sales.iloc[0]['customer_name']} (${top10_sales.iloc[0]['monetary']:,.2f} sales, ${top10_sales.iloc[0]['total_profit']:,.2f} profit)")
print(f"Top Profit Customer: {top10_profit.iloc[0]['customer_name']} (${top10_profit.iloc[0]['total_profit']:,.2f} profit on ${top10_profit.iloc[0]['monetary']:,.2f} sales)")
print(f"High Sales (> $5,000) but Negative Profit: {len(high_sales_neg_profit)} customers")
print(f"At-Risk Segment Accounts: {len(at_risk_customers)} customers (${at_risk_customers['monetary'].sum():,.2f} sales, ${at_risk_customers['total_profit'].sum():,.2f} profit)")

# 8. Reconciliations
reconciled_sales = rfm['monetary'].sum()
reconciled_profit = rfm['total_profit'].sum()
assert len(rfm) == total_unique_customers, "Error: Customer count mismatch"
assert abs(reconciled_sales - total_sales_dataset) < 0.01, "Error: Sales total mismatch"
assert abs(reconciled_profit - total_profit_dataset) < 0.01, "Error: Profit total mismatch"
assert rfm['customer_id'].duplicated().sum() == 0, "Error: Duplicate customer records"
assert rfm['r_score'].isnull().sum() == 0, "Error: Missing R score"
assert rfm['rfm_segment'].isnull().sum() == 0, "Error: Unassigned segments"
print("\n[VALIDATION PASSED] 100% Reconciliation across all customer counts, revenue, and profit totals.")

# ----------------------------------------------------------------------
# 9. RENDER VISUALIZATIONS (Saved to dashboard_images/rfm/)
# ----------------------------------------------------------------------

# Chart 1: Customer Segment Distribution (Bar)
plt.figure(figsize=(9, 5))
bars = plt.barh(seg_summary['rfm_segment'], seg_summary['customer_count'], color='#1F4E79', height=0.6)
plt.title('Customer Count by RFM Segment', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Number of Customers', fontweight='bold')
for bar in bars:
    w = bar.get_width()
    plt.annotate(f"{w} ({w/len(rfm):.1%})", xy=(w, bar.get_y() + bar.get_height()/2),
                 xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '01_rfm_customer_distribution.png'), dpi=300)
plt.close()

# Chart 2: Revenue Contribution by Segment (Donut)
plt.figure(figsize=(8, 8))
plt.pie(seg_summary['total_sales'], labels=seg_summary['rfm_segment'], autopct='%1.1f%%',
        startangle=140, colors=sns.color_palette('Set2', len(seg_summary)),
        wedgeprops=dict(width=0.4, edgecolor='w'))
plt.title('Revenue Contribution (%) by RFM Segment', fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '02_rfm_revenue_contribution.png'), dpi=300)
plt.close()

# Chart 3: Profit Contribution by Segment (Bar)
plt.figure(figsize=(9, 5))
colors = ['#2CA02C' if p >= 0 else '#D62728' for p in seg_summary['total_profit']]
bars = plt.barh(seg_summary['rfm_segment'], seg_summary['total_profit'], color=colors, height=0.6)
plt.title('Net Profit Contribution ($) by RFM Segment', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Net Profit ($)', fontweight='bold')
for bar in bars:
    w = bar.get_width()
    plt.annotate(f"${w:,.0f}", xy=(w, bar.get_y() + bar.get_height()/2),
                 xytext=(5 if w >= 0 else -45, 0), textcoords="offset points", ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '03_rfm_profit_contribution.png'), dpi=300)
plt.close()

# Chart 4: Recency vs Monetary Scatter Plot
plt.figure(figsize=(9, 6))
sns.scatterplot(data=rfm, x='recency', y='monetary', hue='rfm_segment', palette='tab10', alpha=0.8, s=60)
plt.title('Customer Recency vs. Monetary Spend', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Recency (Days Since Last Order)', fontweight='bold')
plt.ylabel('Monetary Value / Lifetime Spend ($)', fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '04_recency_vs_monetary_scatter.png'), dpi=300)
plt.close()

# Chart 5: Frequency vs Monetary Scatter Plot
plt.figure(figsize=(9, 6))
sns.scatterplot(data=rfm, x='frequency', y='monetary', hue='rfm_segment', palette='tab10', alpha=0.8, s=60)
plt.title('Customer Order Frequency vs. Monetary Spend', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Order Frequency (Distinct Orders)', fontweight='bold')
plt.ylabel('Monetary Value / Lifetime Spend ($)', fontweight='bold')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '05_frequency_vs_monetary_scatter.png'), dpi=300)
plt.close()

# Chart 6: Top 10 Customers by Sales
plt.figure(figsize=(9, 5))
plt.barh(top10_sales['customer_name'], top10_sales['monetary'], color='#1F4E79', height=0.6)
plt.gca().invert_yaxis()
plt.title('Top 10 Customers by Total Lifetime Spend', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Sales ($)', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '06_top10_customers_sales.png'), dpi=300)
plt.close()

# Chart 7: Top 10 Customers by Profit
plt.figure(figsize=(9, 5))
plt.barh(top10_profit['customer_name'], top10_profit['total_profit'], color='#2CA02C', height=0.6)
plt.gca().invert_yaxis()
plt.title('Top 10 Customers by Net Profit Contribution', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Total Net Profit ($)', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(rfm_img_dir, '07_top10_customers_profit.png'), dpi=300)
plt.close()

print('All 7 RFM visualizations successfully rendered to dashboard_images/rfm/')
