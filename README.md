# 📊 E-Commerce Commercial & Sales Analytics (End-to-End Enterprise Project)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.30+-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![PowerBI](https://img.shields.io/badge/Power%20BI-DAX%20%26%20Modeling-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, portfolio-ready **Data Analytics & Business Intelligence** project analyzing **9,994 e-commerce transactions** across 4 years (2014–2017). Designed to evaluate revenue drivers, margin degradation thresholds, customer behavioral cohorts, and regional supply chain logistics.

---

## 📌 Executive Summary & Key Performance Indicators (KPIs)

All metrics are **100% empirically derived and reconciled** across Python, SQLite, and Power BI:

```
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐
│     TOTAL REVENUE      │  │       NET PROFIT       │  │     PROFIT MARGIN      │
│     $2,297,200.86      │  │      $286,397.02       │  │         12.47%         │
└────────────────────────┘  └────────────────────────┘  └────────────────────────┘
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐
│      TOTAL ORDERS      │  │      TOTAL UNITS       │  │   AVG ORDER VALUE      │
│         5,009          │  │         37,873         │  │        $458.61         │
└────────────────────────┘  └────────────────────────┘  └────────────────────────┘
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐
│    UNIQUE CUSTOMERS    │  │   AVG DISCOUNT RATE    │  │   AVG SHIPPING DAYS    │
│      793 accounts      │  │         15.62%         │  │       3.96 days        │
└────────────────────────┘  └────────────────────────┘  └────────────────────────┘
```

---

## 🏗️ Project Architecture & Star Schema Data Model

The data pipeline decouples raw data into an optimized **Star Schema** designed for Power BI's in-memory **VertiPaq columnar engine** and relational SQL engines:

```
                         ┌─────────────────────────────┐
                         │         DimCustomer         │
                         │ ─────────────────────────── │
                         │ * customer_id (PK)          │
                         │   customer_name, segment    │
                         │   recency, frequency        │
                         │   monetary, rfm_segment     │
                         └──────────────┬──────────────┘
                                        │ 1
                                        │
                                        │ *
┌────────────────────────┐              │              ┌────────────────────────┐
│       DimProduct       │              │              │      DimGeography      │
│ ────────────────────── │              │              │ ────────────────────── │
│ * product_id (PK)      │ 1            │            1 │ * postal_code (PK)     │
│   category             │──────────────┼──────────────│   city, state          │
│   sub_category         │ *            │            * │   region, country      │
│   product_name         │              │              │                        │
└────────────────────────┘              │              └────────────────────────┘
                                        ▼
                         ┌─────────────────────────────┐
                         │          FactSales          │
                         │ ─────────────────────────── │
                         │ * row_id (PK)               │
                         │   order_id                  │
                         │   order_date (FK)           │
                         │   customer_id (FK)          │
                         │   postal_code (FK)          │
                         │   product_id (FK)           │
                         │   ship_mode_id (FK)         │
                         │   sales, quantity           │
                         │   discount, profit          │
                         │   shipping_days             │
                         └──────────────▲──────────────┘
                                        │ *
                         ┌──────────────┴──────────────┐
                         │ * 1                         │ * 1
          ┌──────────────┴─────────────┐ ┌─────────────┴──────────────┐
          │          DimDate           │ │        DimShipping         │
          │ ────────────────────────── │ │ ────────────────────────── │
          │ * date (PK)                │ │ * ship_mode_id (PK)        │
          │   year, quarter, month     │ │   ship_mode                │
          │   year_month, week, day    │ │   sla_target_days          │
          └────────────────────────────┘ └────────────────────────────┘
```

---

## 📂 Project Repository Structure

```text
Ecommerce-Sales-Analytics/
│
├── data/
│   ├── raw/
│   │   └── Sample_Superstore.csv              # Source immutable dataset (9,994 rows, 21 cols)
│   ├── cleaned/
│   │   ├── superstore_cleaned.csv             # Enriched master dataset (9,994 rows, 28 cols)
│   │   ├── FactSales.csv                      # Fact table (9,994 rows, 17 cols)
│   │   ├── DimCustomer.csv                    # Customer dimension with RFM tags (793 rows)
│   │   ├── DimProduct.csv                     # Product dimension (1,862 rows)
│   │   ├── DimGeography.csv                   # Geography dimension (631 postal codes)
│   │   ├── DimShipping.csv                    # Shipping modes with SLA targets (4 rows)
│   │   └── DimDate.csv                        # Continuous calendar dimension (1,464 dates)
│   ├── analytics/
│   │   └── customer_rfm.csv                   # Customer RFM scores and segment tags
│   └── database/
│       └── superstore.db                      # Indexed SQLite database
│
├── notebooks/
│   ├── 01_data_cleaning_and_quality.ipynb     # Profiling, cleaning & zero-padded zip codes
│   ├── 02_exploratory_data_analysis.ipynb     # Statistical distributions, seasonality & margins
│   └── 03_customer_rfm_analysis.ipynb         # Quintile scoring & RFM behavioral modeling
│
├── sql/
│   ├── 06_business_analysis.sql               # 25 production-grade SQL queries (CTEs, Window Functions)
│   └── query_results/                         # 25 CSV result files from SQL query executions
│
├── reports/
│   ├── data_cleaning_report.md                # Data cleaning log & before-and-after audit
│   ├── eda_report.md                          # Statistical EDA report with Q1–Q10 answers
│   ├── sql_analysis_report.md                 # SQL query results & business interpretations
│   ├── rfm_customer_analysis.md               # RFM customer segmentation report
│   ├── powerbi_data_model.md                  # Star Schema relationship & VertiPaq documentation
│   ├── dax_measures.md                        # 28 production DAX formulas & reconciled values
│   ├── powerbi_dashboard_blueprint.md         # 5-page interactive dashboard wireframes & guide
│   ├── strategic_business_recommendations.md  # 5-Pillar executive recommendations
│   └── resume_and_interview_prep.md           # STAR resume bullet points & interview Q&A
│
├── dashboard_images/                          # 8 High-resolution analytical charts
│   ├── 01_monthly_sales_profit_trend.png
│   ├── 02_category_performance.png
│   ├── 03_subcategory_profitability.png
│   ├── 04_regional_performance.png
│   ├── 05_discount_impact_on_margins.png
│   ├── 06_top10_products_sales.png
│   ├── 07_top10_customers.png
│   └── 08_state_profitability_comparison.png
│
├── dashboard_images/rfm/                      # 7 Customer RFM charts
│   ├── 01_rfm_customer_distribution.png
│   ├── 02_rfm_revenue_contribution.png
│   ├── 03_rfm_profit_contribution.png
│   ├── 04_recency_vs_monetary_scatter.png
│   ├── 05_frequency_vs_monetary_scatter.png
│   ├── 06_top10_customers_sales.png
│   └── 07_top10_customers_profit.png
│
├── scripts/
│   ├── clean_data.py                          # Reproducible data cleaning script
│   ├── run_eda_analysis.py                    # Metric computation script
│   ├── render_eda_charts.py                   # Matplotlib chart generator
│   ├── execute_sql_analysis.py                # SQLite query runner & CSV exporter
│   ├── run_rfm_segmentation.py                # RFM model execution pipeline
│   └── build_powerbi_assets.py                # Star Schema dimension & fact exporter
│
├── requirements.txt                           # Pinned Python dependencies
├── .gitignore                                 # Git configuration
└── README.md                                  # Portfolio documentation
```

---

## 🔍 Key Validated Business Insights

### 1. The 20% Discount Margin Destruction Cliff
* Orders with **0% discount** deliver a **+29.51% profit margin ($320,987.60 profit)**.
* Orders with **1%–20% discount** deliver a **+11.82% margin ($90,337.31 profit)**.
* **Every discount tier above 20% exhibits negative cumulative profit**:
  * `21%–30% discount`: -$10,369.28 profit (-10.05% margin)
  * `31%–40% discount`: -$25,448.19 profit (-19.44% margin)
  * `>40% discount`: -$100,559.41 profit (-81.74% margin)
* Overall, **1,871 transactions (18.72% of all orders)** are loss-making, generating **-$156,131.29 in cumulative losses**.

### 2. Category Performance & Sub-Category Deficits
* **Technology**: **$836,154.03 sales (36.40%)** generated **$145,454.95 profit (50.79% of total company profit)** at a **17.39% margin**.
* **Office Supplies**: **$719,047.03 sales (31.30%)** yielded **$122,490.80 profit (42.77% of company profit)** at a **17.03% margin**.
* **Furniture**: Severe operational drag, generating **$741,999.80 in sales (32.30%)** but yielding only **$18,451.27 in profit (6.44% of company profit)** at a **2.49% margin**, burdened by deficits in **Tables (-$17,725.48)** and **Bookcases (-$3,472.56)**.

### 3. Customer RFM Segmentation & At-Risk VIP Accounts
* **Champions + Loyal Customers** (33.42% of customer base) drive **49.31% of total revenue ($1.13M)**.
* **At-Risk VIP Cohort**: **101 customer accounts (12.74% of base)** that historically drove **$445,804.88 in sales (19.41%)** and **$72,315.11 in profit (25.25%)** at a high **16.22% margin** have been inactive for an average of **268.4 days** (~9 months).
* **Sean Miller Anomaly**: The largest customer by revenue ($25,043.05 spend) generated a **cumulative loss of -$1,980.74** due to deep equipment discounting.

### 4. Regional Profitability & 10 Deficit States
* **West Region** ranks #1 in profitability with **$108,418.45 profit (14.94% margin)**.
* **Top 5 Deficit States**: **Texas (-$25.7K)**, **Ohio (-$17.0K)**, **Pennsylvania (-$15.6K)**, **Illinois (-$12.6K)**, and **North Carolina (-$7.5K)** generated **-$78,359.50 in cumulative losses** due to average localized discount rates between 28.4% and 39.0%.

---

## 💡 Strategic Recommendations & Projected Financial Impact

| Strategic Pillar | Validated Problem Identified | Proposed Tactical Intervention | Projected Annual Profit Impact |
| :--- | :--- | :--- | :--- |
| **1. Discount Capping** | -$156.1K lost in discounts > 20% | Hard-cap standard sales rep discounts at 20%; require VP approval for exceptions. | **+$75,000 to +$100,000 Profit** |
| **2. Furniture Restructuring** | -$21.2K lost in Tables & Bookcases | Require tables to be sold as bundled office suites with high-margin chairs; delist worst 15 SKUs. | **+$15,000 to +$20,000 Profit** |
| **3. At-Risk Account Retention** | $445.8K revenue at risk of lapse | Proactive VIP account manager outreach and automated CRM replenishment triggers. | **+$35,000 to +$50,000 Retained Margin** |
| **4. Regional Deficit Fix** | -$78.4K lost across TX, OH, PA, IL, NC | Eliminate state promo coupon codes; align sales quotas with Gross Margin $ rather than revenue. | **+$35,000 to +$45,000 Profit** |
| **Total Estimated Bottom-Line Uplift** | | | **+$160,000 to +$215,000 Net Profit** |

---

## 🛠️ Technology Stack & Methodologies

* **Python & Pandas**: Automated data ingestion, data type validation, 5-digit postal code zero-padding (`str.zfill(5)`), and Star Schema decoupling.
* **SQL / SQLite**: 25 enterprise analytical queries utilizing Common Table Expressions (CTEs), Window Functions (`DENSE_RANK`, `RANK`, `LAG`, `SUM() OVER`), and running totals.
* **Power BI & DAX**: 5-page dashboard architecture, Star Schema relationship modeling, and 28 production DAX measures (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATESINPERIOD`).
* **RFM Customer Modeling**: Statistical quintile scoring (`pd.qcut`) segmenting 793 accounts into 9 actionable behavioral cohorts.

---

## 🚀 How to Run the Project

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/your-username/Ecommerce-Sales-Analytics.git
cd Ecommerce-Sales-Analytics
pip install -r requirements.txt
```

### 2. Execute Data Pipeline
```bash
# Run data cleaning and export Star Schema tables
python scripts/clean_data.py

# Run statistical EDA & generate charts
python scripts/render_eda_charts.py

# Run SQLite database builder & 25 SQL queries
python scripts/execute_sql_analysis.py

# Run RFM customer segmentation model
python scripts/run_rfm_segmentation.py

# Export Power BI Star Schema dimension CSVs
python scripts/build_powerbi_assets.py
```

### 3. Open in Power BI Desktop
1. Open Power BI Desktop $ightarrow$ **Get Data $ightarrow$ Text/CSV**.
2. Select all CSV files from `data/cleaned/`.
3. In **Model View**, verify 1-to-Many relationships and mark `DimDate` as Date Table.
4. Copy DAX formulas from `reports/dax_measures.md` and follow the layout in `reports/powerbi_dashboard_blueprint.md`.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
