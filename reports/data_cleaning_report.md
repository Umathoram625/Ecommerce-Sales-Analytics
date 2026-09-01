# Data Cleaning & Transformation Report

## Executive Summary
This report documents all data quality issues identified in the raw `Sample_Superstore.csv` dataset, the specific cleaning actions executed, the rationale for each decision, and the before-and-after validation metrics.

---

## 1. Systematic Data Cleaning Log

| # | Field / Area | Issue Identified | Cleaning Action Taken | Business / Analytical Rationale | Affected Rows |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `Column Names` | Inconsistent naming conventions (mixed case, spaces, hyphens). | Normalized all column headers to `lower_snake_case` (e.g., `Order Date` $ightarrow$ `order_date`, `Sub-Category` $ightarrow$ `sub_category`). | Facilitates programmatic access and SQL interoperability without quoting errors. | **All 21 columns** (9,994 rows) |
| **2** | `Order Date` & `Ship Date` | Stored as text / string (`object` dtype) in mixed formats. | Converted to native pandas `datetime64[ns]` using `format='mixed'`. | Enables temporal filtering, time-series analysis, and duration calculations. | **9,994 rows** |
| **3** | `Postal Code` | Stored as numeric `int64`, causing 4-digit East Coast zip codes to lose leading zeros (e.g., `6824` instead of `06824`). | Converted to string and zero-padded to 5 digits using `.astype(str).str.zfill(5)`. | Postal codes are categorical identifiers, not numerical measures; leading zeros are required for accurate geospatial mapping. | **449 rows** (all 9,994 cast to string) |
| **4** | `Duplicate Rows` | Potential repeated transactions or duplicate records. | Ran full-row duplicate check (`df.duplicated().sum()`). | Verified 0 exact duplicate rows exist; preserved all multi-item line orders. | **0 rows removed** (0 true duplicates) |
| **5** | `Missing Values` | Potential null values across records. | Scanned all 21 columns for nulls (`df.isnull().sum()`). | Confirmed 100% complete data across all fields; no imputation required. | **0 rows modified** (0 nulls) |
| **6** | `Profit` Outliers & Deficits | 1,871 transactions exhibited negative profit (down to -$6,599.98). | Retained all 1,871 negative profit transactions without deletion or truncation. | Negative profits represent genuine commercial losses from deep discounting and shipping costs, crucial for profitability analysis. | **1,871 rows preserved** |
| **7** | `Feature Engineering` | Absence of discrete calendar dimensions, fulfillment speed, and margin metrics. | Engineered 7 new columns: `year`, `month`, `month_number`, `quarter`, `year_month`, `shipping_days`, `profit_margin`. | Supports chronological aggregations, fulfillment SLA tracking, and margin analysis. | **9,994 rows** |

---

## 2. Before vs. After Validation Matrix

| Parameter | Raw Dataset (`data/raw/`) | Cleaned Dataset (`data/cleaned/`) | Status |
| :--- | :--- | :--- | :--- |
| **Row Count** | `9,994` | `9,994` | ✅ 100% Retained (0 data loss) |
| **Column Count** | `21` | `28` | ✅ +7 Enriched Analytical Fields |
| **Missing Values** | `0` | `0` | ✅ 100% Complete |
| **Duplicate Rows** | `0` | `0` | ✅ Zero Duplicates |
| **`Order Date` Dtype** | `object (string)` | `datetime64[ns]` | ✅ Native Datetime |
| **`Ship Date` Dtype** | `object (string)` | `datetime64[ns]` | ✅ Native Datetime |
| **`Postal Code` Dtype**| `int64` | `object (string, 5-digit padded)` | ✅ Validated String |
| **Date Range** | `2014-01-03` to `2017-12-30` | `2014-01-03` to `2017-12-30` | ✅ Verified Consistent |
| **Sales Range** | `$0.44` to `$22,638.48` | `$0.44` to `$22,638.48` | ✅ Verified Consistent |
| **Quantity Range** | `1` to `14` units | `1` to `14` units | ✅ Verified Consistent |
| **Discount Range** | `0.00` to `0.80` (0% to 80%) | `0.00` to `0.80` (0% to 80%) | ✅ Verified Consistent |
| **Profit Range** | `-$6,599.98` to `+$8,399.98` | `-$6,599.98` to `+$8,399.98` | ✅ Verified Consistent |
| **Shipping Days** | N/A | `0` to `7` days (Mean = `3.96` days)| ✅ Derived & Validated |
| **Profit Margin** | N/A | `-2.75` to `+0.50` (Ratio) | ✅ Derived & Validated |

---

## 3. Chronological Sorting Validation for `year_month`
* Column `year_month` is formatted as `YYYY-MM` (e.g., `2014-01`, `2014-02`, ..., `2017-12`).
* Because it follows ISO 8601 formatting, lexicographical alphabetical sorting (`A-Z`) is guaranteed to match strict chronological ordering.
