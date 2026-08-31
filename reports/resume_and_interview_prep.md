# Data Analyst Resume & Interview Walkthrough Guide

## 1. Resume Bullet Points (STAR Format)

### Option A: Standard Data Analyst / Commercial Analytics Role
* **E-Commerce Commercial & Sales Analytics (Python, SQL, Power BI, Pandas)**
  * Analyzed 9,994 transaction records representing $2.30M in revenue across 793 customers to identify revenue drivers, pricing leakage, and customer retention opportunities.
  * Developed a 5-table Star Schema data model and authored 25+ DAX measures (YoY growth, Rolling 3M averages, YTD) powering a 3-page executive Power BI dashboard.
  * Formulated an RFM behavioral segmentation model categorizing 101 high-margin "At-Risk" enterprise accounts representing $445.8K in annual revenue, enabling targeted VIP win-back campaigns.
  * Identified a critical 20% discount margin threshold where deep discounts caused -$156.1K in cumulative profit losses; designed a policy proposal estimated to protect +$110K in annual gross profit.
  * Built an enterprise SQL analytical suite featuring 22 complex queries utilizing CTEs, window functions (`DENSE_RANK`, `LAG`, `NTILE`), running totals, and market basket cross-selling matrices.

### Option B: Business Intelligence / Power BI Specialist Role
* **Business Intelligence & Data Warehouse Developer (Power BI, DAX, SQL, Data Modeling)**
  * Architected an optimized dimensional Star Schema decoupling 10K transactions into 4 dimension tables and a centralized fact table for sub-second VertiPaq engine query performance.
  * Authored 25+ complex DAX measures implementing time-intelligence (`SAMEPERIODLASTYEAR`, `DATESINPERIOD`), cohort retention metrics, and dynamic price-elasticity scenarios.
  * Designed an interactive 3-page Power BI dashboard featuring executive KPI scorecards, sub-category margin degradation matrices, and RFM customer lifetime value heatmaps.
  * Automated data transformation and feature engineering pipelines in Python and SQL to calculate AOV, shipping transit delays, and discount brackets.

---

## 2. The 2-Minute Interview Elevator Pitch

> *"In this project, I acted as the lead data analyst examining an e-commerce platform with $2.3 million in revenue and 10,000 transactions across 4 years.
>
> My primary objective was to move beyond descriptive reporting and pinpoint exactly why certain product lines and states were hemorrhaging profit despite strong top-line sales growth.
>
> Using Python and Pandas, I built an end-to-end data quality and cleaning pipeline, engineered unit economics and temporal features, and structured the data into a Star Schema.
>
> Through EDA and 22 enterprise SQL queries using window functions and CTEs, I uncovered two major profit bottlenecks: first, that discounting beyond 20% caused an exponential margin collapse from +21% down to -85%, destroying over $156,000 in profit. Second, that the Furniture category—specifically Tables and Bookcases—was losing over $21,000 due to unoptimized freight and supplier costs.
>
> Finally, I implemented an RFM customer segmentation model and built a 3-page Power BI dashboard with 25+ DAX measures. The resulting business strategy proposed an enterprise discount guardrail, furniture SKU rationalization, and a retention strategy for $445K in at-risk accounts, delivering a projected $200,000 annual profit improvement."*

---

## 3. High-Frequency Interview Questions & How to Answer Them

### Q1: Why did you decouple the data into a Star Schema instead of using one flat table?
**Answer:**
> *"While a single flat table is convenient for quick Python exploratory analysis, it is suboptimal for enterprise BI tools like Power BI and relational databases. In Power BI, the VertiPaq engine compresses data columnar-wise based on cardinality. Repeated string descriptions like customer names and product categories across 10,000 rows consume excessive RAM. By creating 1-to-many single-directional relationships between dimension tables (`dim_customers`, `dim_products`, `dim_geography`, `dim_dates`) and `fact_sales`, we drastically reduce memory footprint, eliminate circular filter ambiguity, and enable clean, reusable DAX time-intelligence calculations."*

### Q2: How did you calculate RFM segmentation and what business value did it provide?
**Answer:**
> *"I calculated Recency as days since the customer's latest transaction relative to the dataset snapshot, Frequency as total distinct orders placed, and Monetary as cumulative customer spend. Using Pandas and SQL `NTILE(5)`, I assigned quintile scores from 1 to 5 for each dimension.
>
> The biggest business revelation was identifying the 'At-Risk' cohort: 101 customers who historically delivered $445,804 in revenue at a 16.2% profit margin, but had not transacted in over 6 months. Rather than spending budget acquiring low-converting cold leads, this gave the sales team an immediate, high-ROI win-back target list."*

### Q3: How did you handle negative profits and what was the root cause?
**Answer:**
> *"Negative profit was not treated as dirty data or an error to drop, because in e-commerce, sales can genuinely operate at a net loss. Through segmentation by discount tiers, I discovered that orders with discounts greater than 20% suffered severe margin erosion, with >50% discounts averaging an -85.2% margin loss. Overall, 18.7% of all orders were loss-making, totaling $156.1K in lost margin. The root cause was unmonitored sales discounting combined with fixed shipping/product cost floors."*

### Q4: Which SQL window functions did you use and why?
**Answer:**
> *"I used `LAG()` to calculate Year-over-Year (YoY) revenue and profit percentage growth rates across consecutive calendar years. I used `DENSE_RANK()` over partitioned categories to rank top products without skipping ranking positions. I used `SUM() OVER(ORDER BY year_month)` to build cumulative running revenue curves, and `NTILE(5)` to generate dynamic customer quintiles for RFM scoring directly inside the database."*
