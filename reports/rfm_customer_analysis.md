# Customer Behavior & RFM Segmentation Report

## Executive Summary
This report presents the customer lifecycle, behavioral segmentation, and customer lifetime value (CLV) findings derived from applying **Recency, Frequency, and Monetary (RFM)** modeling to the 793 unique customer accounts in the validated E-Commerce dataset.

---

## A. Customer Base Overview

* **Total Unique Customer Accounts**: `793`
* **Total Customer Lifetime Revenue**: `$2,297,200.86`
* **Total Customer Lifetime Profit**: `$286,397.02`
* **Average Lifetime Revenue per Customer**: `$2,896.85`
* **Average Lifetime Profit per Customer**: `$361.16`
* **Average Order Frequency per Customer**: `6.32 orders` (Range: 1 to 17 orders)
* **Average Order Value (AOV)**: `$458.61`

---

## B. RFM Methodology

* **Analysis Reference Snapshot Date**: `2017-12-30` (the maximum `order_date` observed in the dataset).
* **Recency (R)**: Number of calendar days between the customer's latest order date and `2017-12-30`.
  * Mean Recency: **151.8 days** (Min = `0 days`, Max = `1,165 days`).
* **Frequency (F)**: Total count of distinct `order_id` transactions placed by the customer.
  * Mean Frequency: **6.32 orders** (Median = `6 orders`).
* **Monetary (M)**: Cumulative dollar sum of `sales` across all line items for that customer.
  * Mean Spend: **$2,896.85** (Min = `$4.83`, Max = `$25,043.05`).

---

## C. Scoring Methodology (Quantile Ranking 1 to 5)

Scores from 1 to 5 are computed using statistical quintiles:

| Score Metric | Direction | Method | Score 1 (Lowest) | Score 5 (Highest) |
| :--- | :--- | :--- | :--- | :--- |
| **Recency Score (R)** | Inverted (Lower days = Higher score) | `pd.qcut(recency, 5)` | Inactive > 286 days | Transacted within $\le$ 30 days |
| **Frequency Score (F)** | Direct (Higher orders = Higher score) | `pd.qcut(rank, 5)` | 1–3 orders | 9–17 orders |
| **Monetary Score (M)** | Direct (Higher spend = Higher score) | `pd.qcut(monetary, 5)` | Spend < $932.50 | Spend > $4,242.00 |

---

## D. RFM Segment Definitions

| RFM Segment | Scoring Criteria | Conceptual Definition |
| :--- | :--- | :--- |
| **Champions** | $R \ge 4, F \ge 4, M \ge 4$ | Most recent buyers, highest order frequency, and top spending accounts. |
| **Loyal Customers** | $R \ge 3, F \ge 3, M \ge 3$ | Consistent repeat purchasers with steady spend and healthy activity. |
| **Potential Loyalists** | $R \ge 4, F \le 2, M \ge 2$ | Recent purchasers with above-average spend but low total order history. |
| **New Customers** | $R \ge 4, F = 1, M = 1$ | First-time buyers acquired within the most recent calendar cycle. |
| **At Risk** | $R \le 2, F \ge 3, M \ge 3$ | High-value, frequent historical buyers who have not purchased in >180 days. |
| **Need Attention** | $R \ge 3, F \le 2, M \le 2$ | Moderately recent buyers with low lifetime spend and low order volume. |
| **About to Sleep** | $R \le 2, F \le 2, M \ge 3$ | Above-average historical spenders with long inactivity and low order counts. |
| **Hibernating** | Moderate $R, F, M$ combinations | Infrequent buyers with below-average spend and moderate recency. |
| **Lost Customers** | $R \le 2, F \le 2, M \le 2$ | Lowest spend, lowest frequency, and inactive for over a year. |

---

## E. Segment-Level Performance Results

| RFM Segment | Customer Count | % Customer Base | Total Sales ($) | % Total Sales | Total Profit ($) | % Total Profit | Profit Margin (%) | Avg Frequency | Avg Recency (Days) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Loyal Customers** | 159 | 20.05% | $572,344.08 | 24.91% | $62,592.76 | 21.86% | 10.94% | 7.9 | 62.8 |
| **Champions** | 106 | 13.37% | $560,498.82 | 24.40% | $67,795.92 | 23.67% | 12.10% | 9.8 | 30.1 |
| **At Risk** | 101 | 12.74% | $445,804.88 | 19.41% | $72,315.11 | 25.25% | 16.22% | 7.4 | 268.4 |
| **Hibernating** | 134 | 16.90% | $242,245.96 | 10.55% | $24,768.04 | 8.65% | 10.22% | 5.2 | 148.9 |
| **About to Sleep** | 54 | 6.81% | $195,050.96 | 8.49% | $28,282.53 | 9.88% | 14.50% | 4.8 | 321.7 |
| **Potential Loyalists**| 53 | 6.68% | $142,318.43 | 6.20% | $21,339.83 | 7.45% | 14.99% | 4.0 | 44.8 |
| **Lost Customers** | 117 | 14.75% | $92,932.05 | 4.05% | $3,656.33 | 1.28% | 3.93% | 3.1 | 465.3 |
| **Need Attention** | 47 | 5.93% | $36,284.89 | 1.58% | $3,841.65 | 1.34% | 10.59% | 3.3 | 66.8 |
| **New Customers** | 22 | 2.77% | $9,720.79 | 0.42% | $1,804.85 | 0.63% | 18.57% | 1.9 | 42.1 |
| **Total / Overall** | **793** | **100.00%** | **$2,297,200.86**| **100.00%** | **$286,397.02** | **100.00%** | **12.47%** | **6.32** | **151.8** |

---

## F. Top Customer Findings

* **Top 5 Revenue Customers**:
  1. `Sean Miller` (Home Office): **$25,043.05 spend** across 8 orders | **-$1,980.74 net loss (-7.91% margin)**
  2. `Tamara Chand` (Corporate): **$19,052.22 spend** across 12 orders | **+$8,981.32 profit (+47.14% margin)**
  3. `Raymond Buch` (Consumer): **$15,117.34 spend** across 10 orders | **+$6,976.10 profit (+46.15% margin)**
  4. `Tom Ashbrook` (Home Office): **$14,595.62 spend** across 10 orders | **+$4,703.79 profit (+32.23% margin)**
  5. `Adrian Barton` (Consumer): **$14,473.57 spend** across 10 orders | **+$5,444.81 profit (+37.62% margin)**

* **Most Frequent Customers**:
  1. `William Brown` (Consumer): **37 transactions across 11 orders** ($3,460.60 spend / $720.17 profit)
  2. `Matt Abelman` (Home Office): **34 transactions across 9 orders** ($4,299.16 spend / $2,007.82 profit)
  3. `John Lee` (Consumer): **34 transactions across 11 orders** ($2,572.33 spend / $602.82 profit)
  4. `Paul Prost` (Consumer): **34 transactions across 11 orders** ($4,642.44 spend / $1,265.40 profit)

---

## G. At-Risk Customer Findings

* **Cohort Scale**: **101 customer accounts (12.74% of customer base)**.
* **Cumulative Revenue**: **$445,804.88 (19.41% of total sales)**.
* **Cumulative Net Profit**: **$72,315.11 (25.25% of total company profit)**.
* **Observed Margin**: **16.22%** (Highest profit margin among high-volume segments).
* **Average Days Inactive**: **268.4 days** (~9 months since latest transaction).
* **Observation**: This group represents historically high-margin, high-frequency buyers who have shown extended periods of transaction inactivity relative to the reference date.

---

## H. Profitability Observations & Anomalies

1. **High-Sales / Loss-Making Accounts**:
   * **17 customer accounts with lifetime spend > $5,000 produced aggregate net losses**.
   * Chief among them: `Sean Miller` (-$1,980.74 loss on $25.0K spend) and `Becky Martin` (-$831.37 loss on $11.7K spend).
2. **Margin Concentration**:
   * **Champions + Loyal Customers + At-Risk** accounts comprise **46.15% of customers** but generate **68.72% of total revenue ($1.58M)** and **70.78% of total net profit ($202.7K)**.

---

## I. Analytical Observations (3-Tier Framework)

### 1. High Revenue & Profit Exposure in the At-Risk Segment
* **Observed Result**: 101 customers representing **$445.8K in sales (19.41%)** and **$72.3K in profit (25.25%)** have an average recency of 268.4 days without a purchase.
* **Possible Explanation**: Extended procurement cycles in B2B corporate purchasing, customer dissatisfaction with prior orders, or competitive vendor switching.
* **Business Implication**: Proactive re-engagement with these 101 verified high-margin accounts offers a high-value retention opportunity compared to cold customer acquisition.

### 2. Profit Disconnection in Selected Top Spenders
* **Observed Result**: The largest customer by revenue (`Sean Miller`, $25.0K sales) incurred a -$1,980.74 net loss.
* **Possible Explanation**: High-value equipment orders purchased under heavy promotional discounts (>50%) where price concessions exceeded the product gross margin.
* **Business Implication**: High gross sales volume does not guarantee profitability; tracking account-level net margin is necessary to evaluate true customer value.

---

## J. Model Validation & Reconciliation Check

| Validation Parameter | Source Dataset (`superstore_cleaned.csv`) | RFM Output (`customer_rfm.csv`) | Status |
| :--- | :--- | :--- | :--- |
| **Unique Customer Count** | `793` | `793` | ✅ Reconciled (100%) |
| **Total Sales Volume** | `$2,297,200.86` | `$2,297,200.86` | ✅ Reconciled (100%) |
| **Total Net Profit** | `$286,397.02` | `$286,397.02` | ✅ Reconciled (100%) |
| **Duplicate Customer IDs**| `0` | `0` | ✅ Zero Duplicates |
| **Missing RFM Scores** | N/A | `0` | ✅ 100% Scored |
| **Unassigned Segments** | N/A | `0` | ✅ 100% Assigned |
