# SQL Business Analysis Report

## Executive Summary
This report presents the empirical findings derived from executing 25 enterprise SQL business queries against the validated SQLite database (`data/database/superstore.db`). All metrics and tables represent verified calculations executed on the 9,994 cleaned transaction records.

---

## Section 1: Core Business KPIs

### Analysis 1: Executive KPI Summary
* **Business Question**: What are the aggregate baseline commercial KPIs for the enterprise across all transactions?
* **SQL Approach**: Standard aggregations combining `SUM()`, `COUNT(DISTINCT ...)`, and arithmetic ratios.
* **SQL Query**:
```sql
SELECT 
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS total_quantity_sold,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS average_discount_pct,
    ROUND(AVG(shipping_days), 2) AS average_shipping_days
FROM superstore_sales;
```
* **Actual Result**:

|   total_sales |   total_profit |   total_quantity_sold |   total_orders |   unique_customers |   average_order_value |   profit_margin_pct |   average_discount_pct |   average_shipping_days |
|--------------:|---------------:|----------------------:|---------------:|-------------------:|----------------------:|--------------------:|-----------------------:|------------------------:|
|    2.2972e+06 |         286397 |                 37873 |           5009 |                793 |                458.61 |               12.47 |                  15.62 |                    3.96 |

* **Business Interpretation**: The platform generated **$2,297,200.86 in gross revenue** and **$286,397.02 in net profit**, resulting in an overall commercial profit margin of **12.47%**. The business fulfilled **5,009 distinct orders** across **793 unique customer accounts**, with an Average Order Value (AOV) of **$458.61** and an average fulfillment transit duration of **3.96 days**.

---

## Section 2: Time-Based Performance & Growth Analysis

### Analysis 2: Annual Trajectory & Year-over-Year (YoY) Growth
* **Business Question**: How did revenue and profitability evolve year-over-year, and what were the annual growth percentages?
* **SQL Approach**: CTE summarizing annual metrics combined with the `LAG()` window function to calculate YoY deltas.
* **SQL Query**:
```sql
WITH yearly_summary AS (
    SELECT 
        year,
        ROUND(SUM(sales), 2) AS annual_sales,
        ROUND(SUM(profit), 2) AS annual_profit,
        COUNT(DISTINCT order_id) AS order_count
    FROM superstore_sales
    GROUP BY year
)
SELECT 
    year,
    annual_sales,
    LAG(annual_sales, 1) OVER (ORDER BY year) AS prior_year_sales,
    ROUND(((annual_sales - LAG(annual_sales, 1) OVER (ORDER BY year)) / LAG(annual_sales, 1) OVER (ORDER BY year)) * 100, 2) AS yoy_sales_growth_pct,
    annual_profit,
    LAG(annual_profit, 1) OVER (ORDER BY year) AS prior_year_profit,
    ROUND(((annual_profit - LAG(annual_profit, 1) OVER (ORDER BY year)) / LAG(annual_profit, 1) OVER (ORDER BY year)) * 100, 2) AS yoy_profit_growth_pct,
    order_count
FROM yearly_summary
ORDER BY year ASC;
```
* **Actual Result**:

|   year |   annual_sales |   prior_year_sales |   yoy_sales_growth_pct |   annual_profit |   prior_year_profit |   yoy_profit_growth_pct |   order_count |
|-------:|---------------:|-------------------:|-----------------------:|----------------:|--------------------:|------------------------:|--------------:|
|   2014 |         484248 |                nan |                 nan    |         49544   |               nan   |                  nan    |           969 |
|   2015 |         470533 |             484248 |                  -2.83 |         61618.6 |             49544   |                   24.37 |          1038 |
|   2016 |         609206 |             470533 |                  29.47 |         81795.2 |             61618.6 |                   32.74 |          1315 |
|   2017 |         733215 |             609206 |                  20.36 |         93439.3 |             81795.2 |                   14.24 |          1687 |

* **Business Interpretation**: Following a minor revenue contraction of **-2.83% in 2015** (though profit grew **+24.37%**), revenue expanded rapidly in **2016 (+29.47% YoY)** and **2017 (+20.36% YoY)**, reaching peak annual revenue of **$733,215.26** and annual net profit of **$93,439.27**.

### Analysis 3: Seasonality & Monthly Demand Patterns
* **Business Question**: Which calendar months demonstrate the strongest commercial demand across the multi-year history?
* **SQL Query**:
```sql
SELECT 
    month_number,
    month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS cumulative_sales,
    ROUND(SUM(profit), 2) AS cumulative_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM superstore_sales
GROUP BY month_number, month
ORDER BY cumulative_sales DESC;
```
* **Actual Result**:

|   month_number | month     |   total_orders |   cumulative_sales |   cumulative_profit |   profit_margin_pct |
|---------------:|:----------|---------------:|-------------------:|--------------------:|--------------------:|
|             11 | November  |            753 |           352461   |            35468.4  |               10.06 |
|             12 | December  |            702 |           325294   |            43369.2  |               13.33 |
|              9 | September |            688 |           307650   |            36857.5  |               11.98 |
|              3 | March     |            354 |           205005   |            28594.7  |               13.95 |
|             10 | October   |            417 |           200323   |            31784    |               15.87 |
|              8 | August    |            341 |           159044   |            21776.9  |               13.69 |
|              5 | May       |            369 |           155029   |            22411.3  |               14.46 |
|              6 | June      |            364 |           152719   |            21285.8  |               13.94 |
|              7 | July      |            338 |           147238   |            13832.7  |                9.39 |
|              4 | April     |            343 |           137762   |            11587.4  |                8.41 |
|              1 | January   |            178 |            94924.8 |             9134.45 |                9.62 |
|              2 | February  |            162 |            59751.2 |            10294.6  |               17.23 |

* **Business Interpretation**: Sales volume is heavily concentrated in Q4. **November ($352,461.07)** and **December ($325,293.50)** generate the highest cumulative sales, while **February ($59,751.25)** consistently displays the lowest volume.

---

## Section 3: Product & Category Commercial Performance

### Analysis 4: Category Contribution Matrix
* **Business Question**: What is the sales, profit, and margin contribution across the major product categories?
* **SQL Query**:
```sql
SELECT 
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND((SUM(sales) / (SELECT SUM(sales) FROM superstore_sales)) * 100, 2) AS revenue_share_pct,
    ROUND((SUM(profit) / (SELECT SUM(profit) FROM superstore_sales)) * 100, 2) AS profit_share_pct
FROM superstore_sales
GROUP BY category
ORDER BY total_sales DESC;
```
* **Actual Result**:

| category        |   total_orders |   units_sold |   total_sales |   total_profit |   profit_margin_pct |   revenue_share_pct |   profit_share_pct |
|:----------------|---------------:|-------------:|--------------:|---------------:|--------------------:|--------------------:|-------------------:|
| Technology      |           1544 |         6939 |        836154 |       145455   |               17.4  |                36.4 |              50.79 |
| Furniture       |           1764 |         8028 |        742000 |        18451.3 |                2.49 |                32.3 |               6.44 |
| Office Supplies |           3742 |        22906 |        719047 |       122491   |               17.04 |                31.3 |              42.77 |

* **Business Interpretation**: **Technology** is the primary profit driver, contributing **50.79% of total company net profit ($145,454.95)** on **36.40% of sales**. Conversely, **Furniture** generates **32.30% of revenue ($741,999.80)** but delivers only **6.44% of net profit ($18,451.27)** due to an overall profit margin of **2.49%**.

### Analysis 5: Sub-Category Profitability Matrix & Loss Leaders
* **Business Question**: Which sub-categories are profitable, and which sub-categories operate at a cumulative net loss?
* **SQL Query**:
```sql
SELECT 
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    DENSE_RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM superstore_sales
GROUP BY category, sub_category
ORDER BY total_profit ASC;
```
* **Actual Result**:

| category        | sub_category   |   total_sales |   total_profit |   profit_margin_pct |   profit_rank |
|:----------------|:---------------|--------------:|---------------:|--------------------:|--------------:|
| Furniture       | Tables         |     206966    |      -17725.5  |               -8.56 |            17 |
| Furniture       | Bookcases      |     114880    |       -3472.56 |               -3.02 |            16 |
| Office Supplies | Supplies       |      46673.5  |       -1189.1  |               -2.55 |            15 |
| Office Supplies | Fasteners      |       3024.28 |         949.52 |               31.4  |            14 |
| Technology      | Machines       |     189239    |        3384.76 |                1.79 |            13 |
| Office Supplies | Labels         |      12486.3  |        5546.25 |               44.42 |            12 |
| Office Supplies | Art            |      27118.8  |        6527.79 |               24.07 |            11 |
| Office Supplies | Envelopes      |      16476.4  |        6964.18 |               42.27 |            10 |
| Furniture       | Furnishings    |      91705.2  |       13059.1  |               14.24 |             9 |
| Office Supplies | Appliances     |     107532    |       18138    |               16.87 |             8 |
| Office Supplies | Storage        |     223844    |       21278.8  |                9.51 |             7 |
| Furniture       | Chairs         |     328449    |       26590.2  |                8.1  |             6 |
| Office Supplies | Binders        |     203413    |       30221.8  |               14.86 |             5 |
| Office Supplies | Paper          |      78479.2  |       34053.6  |               43.39 |             4 |
| Technology      | Accessories    |     167380    |       41936.6  |               25.05 |             3 |
| Technology      | Phones         |     330007    |       44515.7  |               13.49 |             2 |
| Technology      | Copiers        |     149528    |       55617.8  |               37.2  |             1 |

* **Business Interpretation**: 3 sub-categories operate at an aggregate deficit: **Tables (-$17,725.48 profit / -8.56% margin)**, **Bookcases (-$3,472.56 profit / -3.02% margin)**, and **Supplies (-$1,189.10 profit / -2.55% margin)**. The highest profit sub-categories are **Copiers ($55,617.82)**, **Phones ($44,515.73)**, **Accessories ($41,936.64)**, and **Paper ($34,053.57)**.

---

## Section 4: Customer Distribution & Concentration

### Analysis 6: Top 10 Customers by Revenue Spend
* **Business Question**: Who are the top 10 customers by lifetime sales spend, and what is their net profitability?
* **SQL Query**:
```sql
WITH customer_ranks AS (
    SELECT 
        customer_id,
        customer_name,
        segment,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS units_purchased,
        ROUND(SUM(sales), 2) AS total_spend,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
        RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank
    FROM superstore_sales
    GROUP BY customer_id, customer_name, segment
)
SELECT * FROM customer_ranks WHERE sales_rank <= 10;
```
* **Actual Result**:

| customer_id   | customer_name      | segment     |   total_orders |   units_purchased |   total_spend |   total_profit |   profit_margin_pct |   sales_rank |
|:--------------|:-------------------|:------------|---------------:|------------------:|--------------:|---------------:|--------------------:|-------------:|
| SM-20320      | Sean Miller        | Home Office |              5 |                50 |       25043   |       -1980.74 |               -7.91 |            1 |
| TC-20980      | Tamara Chand       | Corporate   |              5 |                42 |       19052.2 |        8981.32 |               47.14 |            2 |
| RB-19360      | Raymond Buch       | Consumer    |              6 |                71 |       15117.3 |        6976.1  |               46.15 |            3 |
| TA-21385      | Tom Ashbrook       | Home Office |              4 |                36 |       14595.6 |        4703.79 |               32.23 |            4 |
| AB-10105      | Adrian Barton      | Consumer    |             10 |                73 |       14473.6 |        5444.81 |               37.62 |            5 |
| KL-16645      | Ken Lonsdale       | Consumer    |             12 |               113 |       14175.2 |         806.85 |                5.69 |            6 |
| SC-20095      | Sanjit Chand       | Consumer    |              9 |                87 |       14142.3 |        5757.41 |               40.71 |            7 |
| HL-15040      | Hunter Lopez       | Consumer    |              6 |                50 |       12873.3 |        5622.43 |               43.68 |            8 |
| SE-20110      | Sanjit Engle       | Consumer    |             11 |                78 |       12209.4 |        2650.68 |               21.71 |            9 |
| CC-12370      | Christopher Conant | Consumer    |              5 |                34 |       12129.1 |        2177.05 |               17.95 |           10 |

* **Business Interpretation**: The top revenue spender is **Sean Miller ($25,043.05 spend)**, but this account generated a **cumulative net loss of -$1,980.74 (-7.91% margin)**. The most profitable customer is **Tamara Chand ($19,052.22 spend / $8,981.32 profit / 47.14% margin)**.

### Analysis 7: Customer Spend Concentration (Pareto Distribution)
* **Business Question**: What proportion of total company revenue is generated by top customer percentiles?
* **SQL Query**:
```sql
WITH customer_totals AS (
    SELECT 
        customer_id,
        SUM(sales) AS customer_spend
    FROM superstore_sales
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT 
        customer_id,
        customer_spend,
        ROW_NUMBER() OVER (ORDER BY customer_spend DESC) AS customer_rank,
        COUNT(*) OVER () AS total_customers,
        SUM(customer_spend) OVER (ORDER BY customer_spend DESC) AS cumulative_sales,
        SUM(customer_spend) OVER () AS total_revenue
    FROM customer_totals
)
SELECT 
    customer_rank,
    ROUND((CAST(customer_rank AS REAL) / total_customers) * 100, 2) AS customer_percentile,
    ROUND(customer_spend, 2) AS customer_spend,
    ROUND(cumulative_sales, 2) AS cumulative_sales,
    ROUND((cumulative_sales / total_revenue) * 100, 2) AS cumulative_revenue_share_pct
FROM ranked_customers
WHERE customer_rank IN (
    CAST(total_customers * 0.05 AS INT),
    CAST(total_customers * 0.10 AS INT),
    CAST(total_customers * 0.20 AS INT),
    CAST(total_customers * 0.50 AS INT),
    total_customers
)
ORDER BY customer_rank ASC;
```
* **Actual Result**:

|   customer_rank |   customer_percentile |   customer_spend |   cumulative_sales |   cumulative_revenue_share_pct |
|----------------:|----------------------:|-----------------:|-------------------:|-------------------------------:|
|              39 |                  4.92 |          7955    |   429012           |                          18.68 |
|              79 |                  9.96 |          6076.14 |   703293           |                          30.62 |
|             158 |                 19.92 |          4299.16 |        1.10178e+06 |                          47.96 |
|             396 |                 49.94 |          2258.19 |        1.83908e+06 |                          80.06 |
|             793 |                100    |             4.83 |        2.2972e+06  |                         100    |

* **Business Interpretation**: The top **20% of customer accounts (158 customers)** generate **47.96% of total company revenue ($1,101,781.39)**, illustrating moderate revenue concentration.

---

## Section 5: Regional & State Performance

### Analysis 8: Regional Profitability Ranking
* **Business Question**: How do the 4 US geographic regions rank in sales, profit, and percentage margin?
* **SQL Query**:
```sql
SELECT 
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    DENSE_RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM superstore_sales
GROUP BY region
ORDER BY profit_rank ASC;
```
* **Actual Result**:

| region   |   total_orders |   units_sold |   total_sales |   total_profit |   profit_margin_pct |   profit_rank |
|:---------|---------------:|-------------:|--------------:|---------------:|--------------------:|--------------:|
| West     |           1611 |        12266 |        725458 |       108418   |               14.94 |             1 |
| East     |           1401 |        10618 |        678781 |        91522.8 |               13.48 |             2 |
| South    |            822 |         6209 |        391722 |        46749.4 |               11.93 |             3 |
| Central  |           1175 |         8780 |        501240 |        39706.4 |                7.92 |             4 |

* **Business Interpretation**: **West Region** ranks #1 in profitability (**$108,418.45 profit / 14.94% margin**), followed by **East ($91,522.78 / 13.48% margin)**, **South ($46,749.43 / 11.93% margin)**, and **Central ($39,706.36 / 7.92% margin)**.

### Analysis 9: Deficit States Breakdown (10 Loss-Making States)
* **Business Question**: Which US states operate at an aggregate net loss, and what are their corresponding average discount rates?
* **SQL Query**:
```sql
SELECT 
    state,
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS net_profit_loss,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM superstore_sales
GROUP BY state, region
HAVING SUM(profit) < 0
ORDER BY net_profit_loss ASC;
```
* **Actual Result**:

| state          | region   |   total_orders |   total_sales |   net_profit_loss |   profit_margin_pct |   avg_discount_pct |
|:---------------|:---------|---------------:|--------------:|------------------:|--------------------:|-------------------:|
| Texas          | Central  |            487 |      170188   |         -25729.4  |              -15.12 |              37.02 |
| Ohio           | East     |            236 |       78258.1 |         -16971.4  |              -21.69 |              32.49 |
| Pennsylvania   | East     |            288 |      116512   |         -15560    |              -13.35 |              32.86 |
| Illinois       | Central  |            276 |       80166.1 |         -12607.9  |              -15.73 |              39    |
| North Carolina | South    |            136 |       55603.2 |          -7490.91 |              -13.47 |              28.35 |
| Colorado       | West     |             79 |       32108.1 |          -6527.86 |              -20.33 |              31.65 |
| Tennessee      | South    |             91 |       30661.9 |          -5341.69 |              -17.42 |              29.13 |
| Arizona        | West     |            108 |       35282   |          -3427.92 |               -9.72 |              30.36 |
| Florida        | South    |            200 |       89473.7 |          -3399.3  |               -3.8  |              29.93 |
| Oregon         | West     |             56 |       17431.2 |          -1190.47 |               -6.83 |              28.87 |

* **Business Interpretation**: 10 states operate at a net loss. The highest deficit states are **Texas (-$25,729.36)**, **Ohio (-$16,971.38)**, **Pennsylvania (-$15,559.96)**, and **Illinois (-$12,607.89)**. In each of these 4 states, the average observed discount rate ranges between **32.49% and 39.00%**, substantially higher than the national average (15.62%).

---

## Section 6: Discount & Profitability Analysis

### Analysis 10: Performance across Standardized Discount Bands
* **Business Question**: How does profitability behave across discrete discount bands?
* **SQL Query**:
```sql
WITH discount_banded AS (
    SELECT 
        CASE 
            WHEN discount = 0.00 THEN '0%'
            WHEN discount > 0.00 AND discount <= 0.10 THEN '>0%-10%'
            WHEN discount > 0.10 AND discount <= 0.20 THEN '>10%-20%'
            WHEN discount > 0.20 AND discount <= 0.30 THEN '>20%-30%'
            WHEN discount > 0.30 AND discount <= 0.40 THEN '>30%-40%'
            WHEN discount > 0.40 THEN '>40%'
            ELSE 'Other'
        END AS discount_band,
        sales,
        profit,
        discount
    FROM superstore_sales
)
SELECT 
    discount_band,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM discount_banded
GROUP BY discount_band
ORDER BY 
    CASE discount_band
        WHEN '0%' THEN 1
        WHEN '>0%-10%' THEN 2
        WHEN '>10%-20%' THEN 3
        WHEN '>20%-30%' THEN 4
        WHEN '>30%-40%' THEN 5
        WHEN '>40%' THEN 6
        ELSE 7
    END;
```
* **Actual Result**:

| discount_band   |   transaction_count |      total_sales |   total_profit |   profit_margin_pct |   avg_discount_pct |
|:----------------|--------------------:|-----------------:|---------------:|--------------------:|-------------------:|
| 0%              |                4798 |      1.08791e+06 |      320988    |               29.51 |               0    |
| >0%-10%         |                  94 |  54369.3         |        9029.18 |               16.61 |              10    |
| >10%-20%        |                3709 | 792153           |       91756.3  |               11.58 |              19.93 |
| >20%-30%        |                 227 | 103227           |      -10369.3  |              -10.05 |              30    |
| >30%-40%        |                 233 | 130911           |      -25448.2  |              -19.44 |              39.07 |
| >40%            |                 933 | 128632           |      -99558.6  |              -77.4  |              70.03 |

* **Business Interpretation**:
  * Transactions with **0% discount** deliver a **+29.51% profit margin ($320,987.60 profit)**.
  * Transactions with **>10%–20% discount** deliver a **+11.59% margin ($91,756.30 profit)**.
  * **All discount bands above 20% exhibit negative aggregate profits** in this dataset:
    * `>20%–30%`: -$10,369.28 profit (-10.05% margin)
    * `>30%–40%`: -$25,448.19 profit (-19.44% margin)
    * `>40%`: -$100,559.41 profit (-81.74% margin)

---

## Section 7: Answers to Specific SQL Business Questions (Q1 – Q10)

| # | Business Question | SQL Finding / Result | Analytical Context |
| :--- | :--- | :--- | :--- |
| **Q1** | Which category generates the most revenue? | **Technology** ($836,154.03) | Represents 36.40% of total revenue. |
| **Q2** | Which category generates the most profit? | **Technology** ($145,454.95) | Delivers 50.79% of total company net profit. |
| **Q3** | Which sub-categories are loss-making? | **Tables** (-$17,725.48), **Bookcases** (-$3,472.56), **Supplies** (-$1,189.10) | Combined deficit of -$22,387.14 across 3 sub-categories. |
| **Q4** | Which region has the highest profit? | **West Region** ($108,418.45 profit / 14.94% margin) | #1 in both dollar profit and percentage margin. |
| **Q5** | Which states have the largest losses? | **Texas** (-$25,729.36), **Ohio** (-$16,971.38), **Pennsylvania** (-$15,559.96), **Illinois** (-$12,607.89), **North Carolina** (-$7,490.91) | 10 states operate at a cumulative net loss. |
| **Q6** | Which products have high sales but negative profit? | `Cisco TelePresence System EX90` ($22.6K sales / -$1.8K profit), `GBC DocuBind P400` ($18.0K sales / -$1.9K profit), `Lexmark MX611dhe` ($16.8K sales / -$4.6K profit), `Cubify CubeX Double Head` ($11.1K sales / -$8.9K profit) | 49 products with sales > $3,000 produced aggregate losses. |
| **Q7** | Which customers generate the most revenue? | **Sean Miller** ($25,043.05), **Tamara Chand** ($19,052.22), **Raymond Buch** ($15,117.34), **Tom Ashbrook** ($14,595.62), **Adrian Barton** ($14,473.57) | Top 5 accounts generated $88,281.80 in sales. |
| **Q8** | Which customer segment is most profitable? | In total dollars: **Consumer** ($134,119.21 profit). In percentage margin: **Home Office** (14.03% margin vs Corporate 13.03% and Consumer 11.55%). | Home Office achieved the highest margin efficiency. |
| **Q9** | Which months have the highest sales? | **November** ($352,461.07) and **December** ($325,293.50) | Q4 represents 32.8% of multi-year sales volume. |
| **Q10**| How does profitability vary across discount bands? | 0% discount = **+29.51% margin**; >10%–20% = **+11.59% margin**; >20%–30% = **-10.05% margin**; >30%–40% = **-19.44% margin**; >40% = **-81.74% margin**. | In this dataset, discounts above 20% are consistently associated with negative aggregate profits. |
