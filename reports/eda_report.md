# Exploratory Data Analysis (EDA) Comprehensive Report

## 1. Dataset Overview
* **Source Dataset**: `data/cleaned/superstore_cleaned.csv`
* **Total Records (Transactions)**: `9,994`
* **Total Features**: `28`
* **Date Range**: `2014-01-03` to `2017-12-30` (1,458 calendar days)
* **Completeness**: 100% (0 missing values, 0 duplicate rows)

---

## 2. Executive Key Performance Indicators (KPIs)

| KPI Metric | Mathematical Formula | Calculated Value |
| :--- | :--- | :--- |
| **Total Revenue** | $\sum(\text{sales})$ | **$2,297,200.86** |
| **Total Net Profit** | $\sum(\text{profit})$ | **$286,397.02** |
| **Overall Profit Margin** | $\frac{\text{Total Profit}}{\text{Total Sales}} \times 100$ | **12.47%** |
| **Total Orders** | $\text{DistinctCount}(\text{order\_id})$ | **5,009** |
| **Total Units Sold** | $\sum(\text{quantity})$ | **37,873 units** |
| **Unique Customers** | $\text{DistinctCount}(\text{customer\_id})$ | **793 accounts** |
| **Average Order Value (AOV)** | $\frac{\text{Total Sales}}{\text{Total Orders}}$ | **$458.61** |
| **Average Discount Rate** | $\text{Mean}(\text{discount}) \times 100$ | **15.62%** |
| **Average Shipping Duration** | $\text{Mean}(\text{shipping\_days})$ | **3.96 days** |

---

## 3. Time-Series & Seasonality Findings

### Annual Trajectory & YoY Growth
* **2014**: Revenue `$484,247.50` | Profit `$49,543.97` | Margin `10.23%`
* **2015**: Revenue `$470,532.51` (-2.83% YoY) | Profit `$61,618.60` (+24.37% YoY) | Margin `13.10%`
* **2016**: Revenue `$609,205.60` (+29.47% YoY) | Profit `$81,795.17` (+32.74% YoY) | Margin `13.43%`
* **2017**: Revenue `$733,215.26` (+20.36% YoY) | Profit `$93,439.27` (+14.24% YoY) | Margin `12.74%`

### Seasonality & Peak Periods
* **Q4 Dominance**: Revenue accelerates heavily in Q4 (October through December), representing **32.8% of total annual sales**.
* **Peak Months**: **November ($352,461.07)** and **December ($325,293.50)** are the highest revenue months across all 4 years.
* **Trough Month**: **February ($59,751.25)** consistently exhibits the lowest sales volume.

---

## 4. Product & Category Findings

### Category Breakdown
* **Technology**: **$836,154.03 sales (36.4%)** | **$145,454.95 profit (50.8% of company profit)** | **17.39% margin**. Primary growth driver.
* **Office Supplies**: **$719,047.03 sales (31.3%)** | **$122,490.80 profit (42.8% of company profit)** | **17.03% margin**. High volume, stable returns.
* **Furniture**: **$741,999.80 sales (32.3%)** | **$18,451.27 profit (only 6.4% of company profit)** | **2.49% margin**. Severe margin drag.

### Sub-Category Profitability Matrix
* **Top Profit Generators**:
  1. `Copiers`: $149,528.03 sales | **$55,617.82 profit (37.20% margin)**
  2. `Phones`: $330,007.05 sales | **$44,515.73 profit (13.49% margin)**
  3. `Accessories`: $167,380.32 sales | **$41,936.64 profit (25.05% margin)**
  4. `Paper`: $78,479.21 sales | **$34,053.57 profit (43.39% margin)**
  5. `Binders`: $203,412.73 sales | **$30,221.76 profit (14.86% margin)**
* **Loss-Making Sub-Categories**:
  1. `Tables`: $206,965.53 sales | **-$17,725.48 profit (-8.56% margin)**
  2. `Bookcases`: $114,880.00 sales | **-$3,472.56 profit (-3.02% margin)**
  3. `Supplies`: $46,673.54 sales | **-$1,189.10 profit (-2.55% margin)**

---

## 5. Customer & Segment Findings

### Customer Spend Concentration
* **793 unique customer accounts**.
* **Average Lifetime Sales per Customer**: `$2,896.85`.
* **Average Lifetime Profit per Customer**: `$361.16`.
* **Pareto Distribution**: The top 20% of customers (158 accounts) account for **47.96% of total company revenue ($1,101,781.39)**.

### Customer Segments
* **Consumer**: **$1,161,401.35 sales (50.56%)** | **$134,119.21 profit** | **11.55% margin**
* **Corporate**: **$706,146.37 sales (30.74%)** | **$91,979.13 profit** | **13.03% margin**
* **Home Office**: **$429,653.15 sales (18.70%)** | **$60,298.68 profit** | **14.03% margin** (Highest margin segment)

---

## 6. Regional & State Findings

### Regional Performance
* **West**: **$725,457.82 sales** | **$108,418.45 profit** | **14.94% margin** (Top region)
* **East**: **$678,781.24 sales** | **$91,522.78 profit** | **13.48% margin**
* **South**: **$391,721.91 sales** | **$46,749.43 profit** | **11.93% margin**
* **Central**: **$501,239.89 sales** | **$39,706.36 profit** | **7.92% margin** (Lowest margin)

### State-Level Deficits
* **10 US states operate at a net financial deficit**:
  1. `Texas`: $170,188.05 sales | **-$25,729.36 profit (-15.12% margin)** | Avg Discount: 37.0%
  2. `Ohio`: $78,258.14 sales | **-$16,971.38 profit (-21.69% margin)** | Avg Discount: 32.5%
  3. `Pennsylvania`: $116,511.91 sales | **-$15,559.96 profit (-13.35% margin)** | Avg Discount: 32.9%
  4. `Illinois`: $80,166.10 sales | **-$12,607.89 profit (-15.73% margin)** | Avg Discount: 39.0%
  5. `North Carolina`: $55,603.16 sales | **-$7,490.91 profit (-13.47% margin)** | Avg Discount: 28.4%
  6. `Colorado`: -$3,566.40 profit
  7. `Tennessee`: -$5,341.69 profit
  8. `Arizona`: -$3,427.97 profit
  9. `Florida`: -$3,399.30 profit
  10. `Oregon`: -$1,190.47 profit

---

## 7. Discount & Profitability Findings

### Empirical Relationship Between Discount & Margin

| Discount Level | Order Count | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :--- | :--- | :--- | :--- | :--- |
| **0.00 (0%)** | 4,798 | $1,087,908.47 | **+$320,987.60** | **+29.51%** |
| **0.10 (10%)** | 94 | $54,369.35 | **+$9,029.18** | **+16.61%** |
| **0.15 (15%)** | 52 | $27,558.52 | **+$1,418.99** | **+5.15%** |
| **0.20 (20%)** | 3,657 | $764,594.37 | **+$90,337.31** | **+11.82%** |
| **0.30 (30%)** | 227 | $103,226.66 | **-$10,369.28** | **-10.05%** |
| **0.32 (32%)** | 27 | $14,493.46 | **-$2,391.14** | **-16.50%** |
| **0.40 (40%)** | 206 | $116,417.78 | **-$23,057.05** | **-19.81%** |
| **0.50 (50%)** | 66 | $58,918.54 | **-$20,506.43** | **-34.80%** |
| **0.70 (70%)** | 418 | $40,620.28 | **-$40,075.36** | **-98.66%** |
| **0.80 (80%)** | 300 | $16,963.76 | **-$30,539.04** | **-180.03%** |

* **Key Finding**: Correlation between discount and profit is negative ($r = -0.219$).
* **Threshold**: At 0%–20% discount, transactions remain consistently profitable. Above 20% discount, every discrete discount tier produces aggregate financial deficits.

---

## 8. Shipping & Fulfillment Findings

| Ship Mode | Avg Days | Min Days | Max Days | Total Sales ($) | Total Profit ($) | Profit Margin (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Same Day** | 0.04 | 0 | 1 | $128,363.13 | $15,891.76 | 12.38% |
| **First Class** | 2.18 | 1 | 4 | $351,428.42 | $48,969.84 | 13.93% |
| **Second Class** | 3.24 | 1 | 5 | $459,193.57 | $57,446.64 | 12.51% |
| **Standard Class**| 5.01 | 3 | 7 | $1,358,215.74 | $164,088.79 | 12.08% |

* **Standard Class** represents **59.1% of total sales volume**.
* Average fulfillment duration is **3.96 days**. All 4 shipping modes maintain consistent, positive margins (12.08% to 13.93%).

---

## 9. Important Analytical Observations (3-Tier Framework)

### Observation A: Margin Collapse Beyond 20% Discount
* **Observed Result**: Transactions with discounts > 20% generate negative cumulative profits across every single tier (e.g. 30% discount = -10.05% margin, 80% discount = -180.03% margin).
* **Possible Explanation**: Fixed product unit costs and fulfillment expenses exceed the heavily reduced selling price; sales volumes do not scale sufficiently to offset unit price degradation.
* **Business Implication**: Higher discount tiers in this dataset are observed to coincide with lower or negative profit margins; capping standard sales discounts at 20% protects company profitability.

### Observation B: Furniture Category Inefficiency
* **Observed Result**: Furniture drives $742K in sales (32.3% of revenue) but yields only $18.5K profit (2.49% margin), with Tables (-$17.7K) and Bookcases (-$3.5K) operating at losses.
* **Possible Explanation**: High freight footprint and heavy discounting on bulky furniture items erode gross margin.
* **Business Implication**: The business is operating a high-revenue, near-zero profit line that consumes substantial inventory capital and logistics overhead.

### Observation C: Geographic Concentration of Losses
* **Observed Result**: 4 states (Texas, Ohio, Pennsylvania, Illinois) account for -$70,868.59 in cumulative profit loss, coinciding with average discount rates exceeding 32%–39%.
* **Possible Explanation**: Regional sales teams in these markets rely excessively on promotional discounts to achieve volume quotas.
* **Business Implication**: Earnings generated in high-margin states (California, New York, Washington) are subsidizing chronic regional deficits in the Central and Eastern territories.

---

## 10. Direct Answers to Business Questions (Q1 - Q10)

* **Q1. Which category generates the most sales?**
  * *Result*: **Technology** ($836,154.03 / 36.4% of total revenue).
  * *Explanation*: Driven by high-ticket items including Copiers and Phones.

* **Q2. Which category generates the most profit?**
  * *Result*: **Technology** ($145,454.95 / 50.8% of total company profit).
  * *Explanation*: Technology delivers the highest profit margin (17.39%) and largest dollar contribution.

* **Q3. Which sub-categories are loss-making?**
  * *Result*: **Tables** (-$17,725.48), **Bookcases** (-$3,472.56), and **Supplies** (-$1,189.10).
  * *Explanation*: These 3 sub-categories destroy a combined -$22,387.14 in profit.

* **Q4. Which region is most profitable?**
  * *Result*: **West Region** ($108,418.45 profit, 14.94% margin).
  * *Explanation*: West leads in both total dollar profit and percentage margin.

* **Q5. Which states generate the highest losses?**
  * *Result*: **Texas** (-$25,729.36), **Ohio** (-$16,971.38), **Pennsylvania** (-$15,559.96), **Illinois** (-$12,607.89), and **North Carolina** (-$7,490.91).
  * *Explanation*: Chronic losses are directly associated with localized average discounts >28%–39%.

* **Q6. Which products generate high sales but poor profit?**
  * *Result*: 
    - `Cisco TelePresence System EX90`: $22,638.48 sales | -$1,811.08 profit
    - `GBC DocuBind P400 Electric Binding System`: $17,965.07 sales | -$1,878.17 profit
    - `Lexmark MX611dhe Laser Printer`: $16,829.90 sales | -$4,589.97 profit
    - `Cubify CubeX 3D Printer Double Head`: $11,099.96 sales | -$8,879.97 profit
  * *Explanation*: High-revenue flagship items that incurred severe losses when sold under promotional pricing.

* **Q7. Which customers contribute the most revenue?**
  * *Result*: **Sean Miller** ($25,043.05), **Tamara Chand** ($19,052.22), **Raymond Buch** ($15,117.34), **Tom Ashbrook** ($14,595.62), **Adrian Barton** ($14,473.57).
  * *Explanation*: Top 5 individual accounts contributed $88,281.80 in sales.

* **Q8. Does higher discount appear associated with lower profitability?**
  * *Result*: **Yes**. Correlation is negative ($r = -0.219$). At 0% discount, margin is +29.51%; at 20% discount, margin is +11.82%; at $\ge$30% discount, every tier produces net negative profit.
  * *Explanation*: Discounts above 20% exceed the available gross margin margin buffer.

* **Q9. Which months have the highest sales?**
  * *Result*: **November** ($352,461.07) and **December** ($325,293.50).
  * *Explanation*: Q4 holiday surges and corporate budget cycle completions drive strong year-end demand.

* **Q10. Which customer segment is most profitable?**
  * *Result*: In absolute dollars: **Consumer** ($134,119.21). In percentage profit margin: **Home Office** (14.03% margin vs Corporate 13.03% and Consumer 11.55%).
  * *Explanation*: Consumer drives the largest volume, but Home Office orders achieve higher margin efficiency.
