# Power BI Star Schema Data Model Architecture

## 1. Executive Summary & Architecture Overview
This document specifies the enterprise **Star Schema data model** designed for Power BI Desktop. The model decouples transaction line items into normalized dimension tables and a centralized fact table, optimizing Power BI's in-memory **VertiPaq columnar database engine** for high compression, sub-second query responsiveness, and unambiguous filter propagation.

```
                         ┌─────────────────────────────┐
                         │         DimCustomer         │
                         │ ─────────────────────────── │
                         │ * customer_id (PK)          │
                         │   customer_name             │
                         │   segment                   │
                         │   recency                   │
                         │   frequency                 │
                         │   monetary                  │
                         │   r_score, f_score, m_score │
                         │   rfm_score, rfm_segment    │
                         └──────────────┬──────────────┘
                                        │ 1
                                        │
                                        │ *
┌────────────────────────┐              │              ┌────────────────────────┐
│       DimProduct       │              │              │      DimGeography      │
│ ────────────────────── │              │              │ ────────────────────── │
│ * product_id (PK)      │ 1            │            1 │ * postal_code (PK)     │
│   category             │──────────────┼──────────────│   city                 │
│   sub_category         │ *            │            * │   state                │
│   product_name         │              │              │   region               │
└────────────────────────┘              │              │   country              │
                                        ▼              └────────────────────────┘
                         ┌─────────────────────────────┐
                         │          FactSales          │
                         │ ─────────────────────────── │
                         │ * row_id (PK)               │
                         │   order_id                  │
                         │   order_date (FK)           │
                         │   ship_date                 │
                         │   ship_mode_id (FK)         │
                         │   customer_id (FK)          │
                         │   postal_code (FK)          │
                         │   product_id (FK)           │
                         │   sales                     │
                         │   quantity                  │
                         │   discount                  │
                         │   profit                    │
                         │   shipping_days             │
                         │   profit_margin             │
                         └──────────────▲──────────────┘
                                        │ *
                         ┌──────────────┴──────────────┐
                         │ * 1                         │ * 1
          ┌──────────────┴─────────────┐ ┌─────────────┴──────────────┐
          │          DimDate           │ │        DimShipping         │
          │ ────────────────────────── │ │ ────────────────────────── │
          │ * date (PK)                │ │ * ship_mode_id (PK)        │
          │   date_key                 │ │   ship_mode                │
          │   year, quarter, month     │ │   sla_target_days          │
          │   month_number, year_month │ │   delivery_tier            │
          │   week_number, day_of_week │ └────────────────────────────┘
          │   is_weekend               │
          └────────────────────────────┘
```

---

## 2. Table Specifications & Schema Definitions

### Fact Table: `FactSales` (9,994 Rows)
* **Grain**: One record per individual transaction line item within a customer order.
* **Primary Key**: `row_id`
* **Foreign Keys**: `order_date` (to `DimDate[date]`), `customer_id` (to `DimCustomer[customer_id]`), `product_id` (to `DimProduct[product_id]`), `postal_code` (to `DimGeography[postal_code]`), `ship_mode_id` (to `DimShipping[ship_mode_id]`).
* **Measures / Metrics**: `sales`, `quantity`, `discount`, `profit`, `shipping_days`, `profit_margin`.

### Dimension Table: `DimCustomer` (793 Rows)
* **Grain**: One record per unique customer account.
* **Primary Key**: `customer_id`
* **Attributes**: `customer_name`, `segment`, `recency`, `frequency`, `monetary`, `r_score`, `f_score`, `m_score`, `rfm_score`, `rfm_segment`.

### Dimension Table: `DimProduct` (1,862 Rows)
* **Grain**: One record per unique product SKU.
* **Primary Key**: `product_id`
* **Attributes**: `category`, `sub_category`, `product_name`.

### Dimension Table: `DimGeography` (631 Rows)
* **Grain**: One record per unique US 5-digit postal code.
* **Primary Key**: `postal_code`
* **Attributes**: `city`, `state`, `region`, `country`.

### Dimension Table: `DimShipping` (4 Rows)
* **Grain**: One record per fulfillment shipping tier.
* **Primary Key**: `ship_mode_id`
* **Attributes**: `ship_mode`, `sla_target_days`, `delivery_tier`.

### Dimension Table: `DimDate` (1,464 Rows)
* **Grain**: One record per continuous calendar day from `2014-01-03` to `2018-01-05`.
* **Primary Key**: `date`
* **Attributes**: `date_key`, `year`, `quarter`, `year_quarter`, `month_number`, `month`, `month_short`, `year_month`, `week_number`, `day`, `day_of_week`, `day_of_week_num`, `is_weekend`.

---

## 3. Relationship & Cardinality Mapping

| From (Dimension) | Primary Key (PK) | To (Fact) | Foreign Key (FK) | Cardinality | Cross-Filter Direction | Relationship Type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `DimDate` | `date` | `FactSales` | `order_date` | `1 : Many (1:*)` | **Single** (Dim $ightarrow$ Fact) | **Active** |
| `DimDate` | `date` | `FactSales` | `ship_date` | `1 : Many (1:*)` | **Single** (Dim $ightarrow$ Fact) | **Inactive** (use `USERELATIONSHIP`) |
| `DimCustomer` | `customer_id` | `FactSales` | `customer_id` | `1 : Many (1:*)` | **Single** (Dim $ightarrow$ Fact) | **Active** |
| `DimProduct` | `product_id` | `FactSales` | `product_id` | `1 : Many (1:*)` | **Single** (Dim $ightarrow$ Fact) | **Active** |
| `DimGeography` | `postal_code` | `FactSales` | `postal_code` | `1 : Many (1:*)` | **Single** (Dim $ightarrow$ Fact) | **Active** |
| `DimShipping` | `ship_mode_id`| `FactSales` | `ship_mode_id`| `1 : Many (1:*)` | **Single** (Dim $ightarrow$ Fact) | **Active** |

---

## 4. Star Schema Technical Justification

1. **VertiPaq Columnar Compression**:
   * Repeated text strings (e.g., product names, customer segments, state names) are stored once in dimension dictionaries rather than repeated 10,000 times in the fact table, minimizing memory RAM consumption.
2. **Single-Direction Filter Flow**:
   * Eliminates circular dependency ambiguity and bidirectional filter performance penalties. Filters applied to any dimension propagate naturally down into `FactSales`.
3. **Time Intelligence Compatibility**:
   * `DimDate` provides a contiguous, unbroken calendar required for DAX time-intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATESINPERIOD`).
4. **Sort-By Column Configuration**:
   * `DimDate[month]` is sorted by `DimDate[month_number]`.
   * `DimDate[year_month]` sorts chronologically due to `YYYY-MM` ISO formatting.
