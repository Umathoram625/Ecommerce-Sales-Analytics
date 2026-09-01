# Power BI Dashboard Architecture & Blueprint

## Executive Overview
This document specifies the interactive UI wireframes, visual components, filter interactions, tooltips, drill-through pathways, and implementation steps for building the **5-Page Power BI Executive Dashboard**.

---

## 5-Page Dashboard Architecture

### Page 1: Executive Sales Overview
* **Objective**: High-level commercial scorecard for executive leadership (CEO, CFO, VP Sales).
* **Visuals**:
  1. **Top KPI Cards (5 Cards)**:
     - `Total Sales` ($2.30M) with YoY indicator
     - `Total Profit` ($286.4K) with YoY indicator
     - `Profit Margin %` (12.5%)
     - `Total Orders` (5,009)
     - `Average Order Value` ($458.61)
  2. **Main Visual (Left 60%)**: `Line and Clustered Column Chart`
     - X-Axis: `DimDate[year_month]`
     - Column: `[Total Sales]`
     - Line: `[Total Profit]`
     - Trendline: `[Sales 3M Rolling Avg]`
  3. **Category Contribution (Right Top 40%)**: `Donut Chart`
     - Legend: `DimProduct[category]`
     - Values: `[Total Sales]`
     - Tooltip: `[Profit Margin %]`, `[Total Profit]`
  4. **Regional Revenue & Profit (Right Bottom 40%)**: `Clustered Bar Chart`
     - Y-Axis: `DimGeography[region]`
     - X-Axis: `[Total Sales]` & `[Total Profit]`
  5. **Slicers (Top Ribbon)**: `DimDate[year]`, `DimGeography[region]`, `DimCustomer[segment]`.

---

### Page 2: Sales & Profitability Deep-Dive
* **Objective**: Detailed diagnostic of margin degradation, discounting impact, and loss-making transactions.
* **Visuals**:
  1. **KPI Risk Cards (3 Cards)**:
     - `Average Discount %` (15.6%) | `Loss Order Rate %` (18.7%) | `Loss-Making Sales` ($468.7K)
  2. **Discount vs. Profit Margin Matrix (Left 50%)**: `Clustered Column Chart`
     - X-Axis: Discount Bands (`0%`, `>0%-10%`, `>10%-20%`, `>20%-30%`, `>30%-40%`, `>40%`)
     - Column: `[Profit Margin %]` (Conditionally formatted: Green $\ge 0$, Red $< 0$)
     - Line: `[Total Sales]`
  3. **Sub-Category Profitability Diverging Bar (Right 50%)**: `Horizontal Bar Chart`
     - Y-Axis: `DimProduct[sub_category]`
     - X-Axis: `[Total Profit]`
     - Conditional Formatting: Red for negative profit sub-categories (Tables, Bookcases, Supplies).
  4. **Bottom Loss-Making Order Audit Table (Bottom Full-Width)**: `Table Visual`
     - Columns: `order_id`, `product_name`, `state`, `sales`, `discount`, `profit`, `profit_margin`.

---

### Page 3: Customer Behavior & RFM Segmentation
* **Objective**: Customer lifetime value, retention cohorts, and churn risk management.
* **Visuals**:
  1. **Customer Cohort KPIs (4 Cards)**:
     - `Total Customers` (793) | `Repeat Customer %` (98.4%) | `At Risk Sales` ($445.8K) | `At Risk Profit` ($72.3K)
  2. **RFM Segment Distribution (Left 50%)**: `Treemap Visual`
     - Group: `DimCustomer[rfm_segment]`
     - Values: `[Total Sales]`
     - Tooltip: `[Total Customers]`, `[Profit Margin %]`
  3. **Customer Recency vs. Spend Scatter (Right 50%)**: `Scatter Chart`
     - X-Axis: `DimCustomer[recency]` (Days)
     - Y-Axis: `DimCustomer[monetary]` (Spend)
     - Legend / Color: `DimCustomer[rfm_segment]`
     - Size: `DimCustomer[frequency]`
  4. **Top & At-Risk Customer Account Grid (Bottom Full-Width)**: `Matrix Visual`
     - Rows: `customer_name`, `segment`, `rfm_segment`
     - Values: `[Total Sales]`, `[Total Profit]`, `[Total Orders]`, `[Profit Margin %]`.

---

### Page 4: Product & Category Performance
* **Objective**: Merchandising mix, SKU volume rankings, and catalog rationalization.
* **Visuals**:
  1. **Category Performance Table (Top Left 50%)**: `Matrix Visual`
     - Rows: `category` $ightarrow$ `sub_category`
     - Values: `[Total Sales]`, `[Total Profit]`, `[Total Quantity]`, `[Profit Margin %]`
  2. **Top 10 Products by Revenue (Top Right 50%)**: `Bar Chart`
     - Y-Axis: `DimProduct[product_name]` (Top 10 filter)
     - X-Axis: `[Total Sales]`
  3. **High-Sales / Loss-Making Product Audit (Bottom Full-Width)**: `Table Visual`
     - Filter: `[Total Sales] > $3,000` and `[Total Profit] < 0`
     - Columns: `product_name`, `category`, `sub_category`, `sales`, `profit`, `profit_margin`.

---

### Page 5: Regional & Shipping Logistics Analysis
* **Objective**: Geographic performance, state-level deficits, and fulfillment SLA tracking.
* **Visuals**:
  1. **Geographic State Map (Left 50%)**: `Shape Map / Filled Map`
     - Location: `DimGeography[state]`
     - Color Saturation: `[Total Profit]` (Diverging Red-Yellow-Green)
     - Tooltip: `[Total Sales]`, `[Average Discount %]`
  2. **State Deficit Table (Top Right 50%)**: `Table Visual`
     - Filter: `[Total Profit] < 0`
     - Columns: `state`, `region`, `total_sales`, `total_profit`, `avg_discount_pct`
  3. **Ship Mode SLA Performance (Bottom Right 50%)**: `Clustered Bar Chart`
     - Y-Axis: `DimShipping[ship_mode]`
     - X-Axis: `[Avg Shipping Days]` vs `RELATED(DimShipping[sla_target_days])`
     - Tooltip: `[Total Sales]`, `[Profit Margin %]`.

---

## 6. Step-by-Step Power BI Desktop Implementation Guide

### Step 1: Ingest Data
1. Launch Power BI Desktop.
2. Click **Get Data $ightarrow$ Text/CSV**.
3. Select and import the 6 files from `data/cleaned/`:
   - `DimCustomer.csv`
   - `DimProduct.csv`
   - `DimGeography.csv`
   - `DimShipping.csv`
   - `DimDate.csv`
   - `FactSales.csv`

### Step 2: Configure Model Relationships
1. Navigate to the **Model View** tab.
2. Verify / create the 1-to-Many single-direction relationships:
   - `DimDate[date]` $ightarrow$ `FactSales[order_date]`
   - `DimCustomer[customer_id]` $ightarrow$ `FactSales[customer_id]`
   - `DimProduct[product_id]` $ightarrow$ `FactSales[product_id]`
   - `DimGeography[postal_code]` $ightarrow$ `FactSales[postal_code]`
   - `DimShipping[ship_mode_id]` $ightarrow$ `FactSales[ship_mode_id]`
3. Right-click `DimDate` $ightarrow$ **Mark as Date Table** $ightarrow$ select `date` column.

### Step 3: Create Key Measures
1. Click **Enter Data** $ightarrow$ create an empty table named `_Measures`.
2. Copy and paste the 28 DAX formulas from `reports/dax_measures.md`.

### Step 4: Build Visual Pages
1. Follow the exact visual layouts, slicers, and conditional formatting rules specified in Sections 1 through 5 of this blueprint.
