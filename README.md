# 📊 E-Commerce Sales & Profitability Analytics

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![SQL](https://img.shields.io/badge/SQL-ANSI%20%7C%20MySQL%20%7C%20Postgres-orange.svg)](https://en.wikipedia.org/wiki/SQL)
[![PowerBI](https://img.shields.io/badge/Power%20BI-DAX%20%26%20Modeling-yellow.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

An enterprise-grade, portfolio-ready Data Analytics project analyzing e-commerce transactions, gross revenue drivers, margin degradation points, customer lifecycle cohorts, and regional logistics efficiency.

---

## 📌 Executive Summary

This end-to-end data analytics project examines **9,994 transactions** generating **$2,297,200.86 in revenue** and **$286,397.02 in net profit** (12.47% overall profit margin).

### 🎯 Key Performance Indicators (KPIs)
* **Total Revenue:** `$2,297,200.86`
* **Total Net Profit:** `$286,397.02`
* **Overall Profit Margin:** `12.47%`
* **Total Orders:** `5,009`
* **Total Quantity Sold:** `37,873 units`
* **Total Customers:** `793 unique accounts`
* **Average Order Value (AOV):** `$458.61`

---

## 🏗️ Project Architecture & Star Schema

The project architecture separates raw ingestion from processed analytics and organizes data into a **Star Schema** optimized for Power BI's VertiPaq engine and relational SQL queries.

```
Ecommerce-Sales-Analytics/
│
├── data/
│   ├── raw/
│   │   └── Sample_Superstore.csv              # Source raw transaction data
│   └── cleaned/
│       ├── superstore_cleaned.csv             # Cleaned & feature-engineered dataset (9,994 rows)
│       ├── customer_rfm_segments.csv          # RFM scores and customer cohorts
│       ├── dim_customers.csv                  # Customer dimension table (793 customers)
│       ├── dim_products.csv                   # Product dimension table (1,862 SKUs)
│       ├── dim_geography.csv                  # Geographic dimension table (632 postal codes)
│       ├── dim_dates.csv                      # Calendar dimension table (1,464 dates)
│       └── fact_sales.csv                     # Sales transaction fact table
│
├── notebooks/
│   ├── 01_data_cleaning_and_quality.ipynb     # Profiling, cleaning, outlier handling & Star Schema
│   ├── 02_exploratory_data_analysis.ipynb     # Statistical EDA, distributions & business trends
│   └── 03_customer_rfm_segmentation.ipynb     # RFM model, quintile scoring & behavioral clusters
│
├── sql/
│   ├── 01_schema_setup.sql                    # DDL schemas, primary/foreign keys & indexes
│   ├── 02_data_ingestion.sql                  # Bulk ingestion scripts (MySQL & PostgreSQL)
│   └── 03_business_analysis_queries.sql       # 22 enterprise business queries (CTEs, Window Functions, YoY)
│
├── powerbi/
│   ├── data_model_architecture.md             # Star schema mapping & relationship definitions
│   ├── dax_measures_library.md                # 25+ DAX calculations (YTD, YoY, Margins, AOV, Cohorts)
│   └── dashboard_design_guide.md              # 3-page wireframe layouts, visual rules & color palette
│
├── reports/
│   ├── executive_summary_report.md            # C-level executive briefing with quantified metrics
│   └── business_recommendations.md            # Tactical 3-part Action Plan (What / Why / Action)
│
├── dashboard_images/                          # Visual charts, trend plots & dashboard assets
├── requirements.txt                           # Pinned Python library dependencies
├── .gitignore                                 # Git ignore configuration
└── README.md                                  # Comprehensive portfolio documentation
```

---

## 🔍 Key Business Findings

### 1. The Discount Margin Destruction Threshold (>20%)
* Orders discounted between **0%–20%** maintain strong profitability (**21.0% to 30.0% profit margin**).
* Discounts beyond 20% experience severe negative margin returns: **21%–50% discount** produces **-18.5% margin**, while **>50% discount** collapses to **-85.2% margin**.
* In total, **1,871 transactions (18.72% of all orders)** are loss-making, generating **-$156,128.33 in cumulative financial losses**.

### 2. Category Profitability Breakdown
* **Technology**: Top profit contributor generating **$836.2K sales**, **$145.5K profit** (**17.39% margin**).
* **Office Supplies**: High-volume, reliable returns with **$719.0K sales**, **$122.5K profit** (**17.03% margin**).
* **Furniture**: Severe operational drag with **$742.0K sales** but only **$18.5K net profit** (**2.49% margin**), burdened by heavy losses in **Tables (-$17.7K)** and **Bookcases (-$3.5K)**.

### 3. Customer RFM Segmentation & Churn Risk
* **Champions & Loyal Customers** (33.4% of base) generate **49.3% of total revenue ($1.13M)**.
* **At-Risk VIP Accounts**: **101 customers** representing **$445,804.88 in revenue (19.4%)** with an attractive **16.22% margin** have not transacted in >180 days.

### 4. Regional Deficits
* **West Region** leads with **$108.4K profit** (14.9% margin).
* **10 Deficit States**: Texas (-$25.7K), Ohio (-$17.0K), Pennsylvania (-$15.6K), and Illinois (-$12.6K) operate at deep net losses due to excessive localized discounting (>32%–38% average discount).

---

## 💡 Strategic Recommendations (Action Plan)

| Area | What Happened? | Why It Matters? | Recommended Action |
| :--- | :--- | :--- | :--- |
| **Pricing Policy** | Discounts >20% destroy -$156.1K in profit | Deep discounting subsidizes unprofitable orders | Hard-cap sales rep discounts at 20% in ERP/CRM; require VP approval for exceptions. |
| **Merchandising** | Tables and Bookcases lost -$21.2K | High shipping/freight costs consume all gross margin | Renegotiate vendor costs, bundle with high-margin chairs, delist bottom 15 loss SKUs. |
| **CRM / Retention** | 101 At-Risk accounts hold $445.8K revenue | Losing existing high-margin buyers is 5x more costly than acquisition | Deploy proactive VIP account manager win-back outreach and automated replenishment triggers. |
| **Regional Sales** | TX, OH, PA, IL generate -$70.8K loss | Local promotions diluting regional earnings | Eliminate state auto-promos and align sales bonuses to Gross Margin $ rather than revenue. |

---

## 🛠️ SQL Business Analysis Suite (22 Queries)

The `sql/03_business_analysis_queries.sql` script contains 22 production-grade SQL queries answering specific commercial questions:

* **Executive Performance**: Total Revenue, Margins, AOV, YoY Growth, 3-Month Rolling Average, Running Cumulative Totals.
* **Product & Category Matrix**: Sub-category contribution % to parent category, Top 10 Best Sellers (`DENSE_RANK`), Bottom 10 Loss Leaders.
* **Pricing & Discounts**: Margin degradation across discount brackets, Deep discount outlier audit.
* **Geographic Insights**: Regional rank by profit, Bottom 10 deficit states, Top 10 profitable cities.
* **Customer Lifetime & RFM**: Pure SQL RFM Scoring using `NTILE(5)`, Pareto 80/20 customer analysis, Repeat purchase cohort retention.
* **Logistics & Baskets**: Shipping duration vs mode, Transit delays (>5 days), Market basket cross-selling analysis.

---

## 📊 Power BI Dashboard & DAX Measures

The `powerbi/` directory includes:
* **Star Schema Architecture**: Documented 1-to-many relationship mapping.
* **DAX Measures Library**: 25+ DAX calculations covering Base KPIs, Time Intelligence (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATESINPERIOD`), Customer Analytics, and Margin Protection.
* **Dashboard Design Guide**: 3-page layout wireframes, slicer configuration, and color hierarchy.

---

## 🚀 How to Run the Project

### Prerequisites
* Python 3.10+
* Git

### Installation & Execution
```bash
# 1. Clone repository
git clone https://github.com/username/Ecommerce-Sales-Analytics.git
cd Ecommerce-Sales-Analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Data Cleaning & Star Schema Pipeline
jupyter notebook notebooks/01_data_cleaning_and_quality.ipynb

# 4. Run Exploratory Data Analysis (EDA)
jupyter notebook notebooks/02_exploratory_data_analysis.ipynb

# 5. Run Customer RFM Segmentation
jupyter notebook notebooks/03_customer_rfm_segmentation.ipynb
```

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
