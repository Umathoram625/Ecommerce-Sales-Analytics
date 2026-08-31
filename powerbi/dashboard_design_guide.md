# Power BI Dashboard Design & Implementation Guide

## Executive Overview
This guide specifies the layout, visual hierarchy, color palette, and interactive slicer architecture for the 3-page interactive Power BI report: **E-Commerce Commercial & Operational Intelligence Dashboard**.

---

## Color Palette & Visual Theme
- **Primary / Corporate Blue**: `#1F4E79` (Headers, main charts, standard metrics)
- **Profit / Success Green**: `#2CA02C` (Positive profits, YoY growth, margins)
- **Loss / Alert Red**: `#D62728` (Loss-making products/states, deep discount erosion)
- **Secondary Accent**: `#4682B4` (Comparison bars, categorical fills)
- **Background**: `#F8F9FA` (Clean executive white/light grey canvas)
- **Card Background**: `#FFFFFF` (White tiles with subtle 1px border `#E0E0E0`)

---

## 3-Page Dashboard Layout Architecture

### Page 1: Executive Sales & Profitability Overview
*Target Audience: C-Suite, VP of Sales, Commercial Finance*

1. **Top KPI Bar (5 Cards)**:
   - Card 1: `Total Revenue` ($2.30M) + YoY Growth %
   - Card 2: `Total Profit` ($286.4K) + YoY Growth %
   - Card 3: `Profit Margin %` (12.5%)
   - Card 4: `Total Orders` (5,009)
   - Card 5: `Average Order Value (AOV)` ($458.61)
2. **Main Chart (Left 60%)**:
   - `Line & Clustered Column Chart`: Monthly Sales ($ Bars) vs Net Profit ($ Line) across 48 months with 3M rolling average trendline.
3. **Category Breakdown (Right 40% Top)**:
   - `Donut / Horizontal Bar Chart`: Revenue and Profit Margin by Category (Technology: $836K / 17.4% margin, Office Supplies: $719K / 17.0% margin, Furniture: $742K / 2.5% margin).
4. **Geographic Regional Map (Right 40% Bottom)**:
   - `Filled Map / Clustered Bar`: Sales & Profit by US Region (West leading with $108.4K profit).
5. **Top Slicers**: `Order Year` (2014-2017), `Region`, `Segment`, `Category`.

---

### Page 2: Product Performance & Discount Risk Audit
*Target Audience: Category Managers, Pricing Analysts, Merchandising Directors*

1. **Top KPI Summary**:
   - `Average Discount %` (15.6%) | `Loss-Making Orders Rate` (18.7%) | `Total Unprofitable Losses` (-$156.1K)
2. **Sub-Category Profitability Matrix (Left Top)**:
   - `Diverging Bar Chart`: Profit by Sub-Category. Red highlighting for negative categories (Tables: -$17.7K, Bookcases: -$3.5K, Supplies: -$1.2K).
3. **Discount Sensitivity vs Profit Margin (Left Bottom)**:
   - `Column Chart`: Profit Margin % by Discount Bracket (`0%` -> 30.0% margin, `1-20%` -> 21.0% margin, `21-50%` -> -18.5% margin, `>50%` -> -85.2% margin).
4. **Top 10 vs Bottom 10 Products (Right Side Table / Visual)**:
   - Interactive matrix with conditional formatting showing top revenue generators alongside bottom loss leaders.
5. **Filters**: `Sub-Category`, `Discount Bracket`, `State`, `Ship Mode`.

---

### Page 3: Customer Behavior & RFM Segmentation
*Target Audience: CMO, Growth Leads, CRM Managers*

1. **Customer Cohort Metrics**:
   - `Total Customers` (793) | `Repeat Customer Rate` (98.4%) | `Revenue per Customer` ($2,896.85)
2. **RFM Customer Segmentation Treemap / Donut (Left Top)**:
   - Visual breakdown of customers by cohort: *Champions*, *Loyal Customers*, *Potential Loyalists*, *At Risk*, *Lost*.
3. **Revenue Contribution by Cohort (Left Bottom)**:
   - Bar chart displaying spend distribution ($572K Loyal, $560K Champions, $445K At Risk).
4. **Top High-Value Customers Table (Right Side)**:
   - Detailed customer rank, lifetime spend, order frequency, recency, and segment tag.
5. **Action Filter**: Filter by `Customer Segment` to export target campaign lists.
