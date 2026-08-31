# Power BI Data Model Architecture

## Star Schema Overview
This analytical data model implements an enterprise-grade **Star Schema** architecture designed to optimize Power BI's in-memory **VertiPaq engine**, ensuring sub-second visual rendering, clean measure calculations, and high maintainability.

```
                  ┌──────────────────────┐
                  │    dim_customers     │
                  │ ──────────────────── │
                  │ * customer_id (PK)   │
                  │   customer_name      │
                  │   segment            │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ *
┌────────────────────┐       │       ┌────────────────────┐
│    dim_products    │       │       │   dim_geography    │
│ ────────────────── │       │       │ ────────────────── │
│ * product_id (PK)  │ 1     │     1 │ * postal_code (PK) │
│   category         │───────┼───────│   city             │
│   sub_category     │ *     │     * │   state            │
│   product_name     │       │       │   region           │
└────────────────────┘       │       │   country          │
                             ▼       └────────────────────┘
                  ┌──────────────────────┐
                  │      fact_sales      │
                  │ ──────────────────── │
                  │ * row_id (PK)        │
                  │   order_id           │
                  │   order_date (FK)    │
                  │   ship_date          │
                  │   ship_mode          │
                  │   customer_id (FK)   │
                  │   postal_code (FK)   │
                  │   product_id (FK)    │
                  │   sales              │
                  │   quantity           │
                  │   discount           │
                  │   profit             │
                  │   shipping_duration  │
                  │   unit_price         │
                  │   unit_cost          │
                  │   profit_margin_pct  │
                  │   is_profitable      │
                  │   discount_bracket   │
                  └──────────▲───────────┘
                             │ *
                             │
                             │ 1
                  ┌──────────┴───────────┐
                  │      dim_dates       │
                  │ ──────────────────── │
                  │ * date (PK)          │
                  │   date_id            │
                  │   year               │
                  │   quarter            │
                  │   month              │
                  │   month_name         │
                  │   day                │
                  │   day_name           │
                  │   is_weekend         │
                  └──────────────────────┘
```

---

## Table Schemas & Cardinality Mappings

| From (Dimension Table) | PK Column | To (Fact Table) | FK Column | Cardinality | Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dim_dates` | `date` | `fact_sales` | `order_date` | `1 : Many (1:*)` | Single (Dimension to Fact) |
| `dim_customers` | `customer_id` | `fact_sales` | `customer_id` | `1 : Many (1:*)` | Single (Dimension to Fact) |
| `dim_products` | `product_id` | `fact_sales` | `product_id` | `1 : Many (1:*)` | Single (Dimension to Fact) |
| `dim_geography` | `postal_code` | `fact_sales` | `postal_code` | `1 : Many (1:*)` | Single (Dimension to Fact) |

---

## Best Practices Implemented
1. **Single-Direction Filtering**: All relationships filter from Dimension (1) to Fact (*). Bidirectional filtering is strictly avoided to prevent ambiguous filter paths and performance degradation.
2. **Dedicated Date Dimension**: `dim_dates` is flagged as an official Date Table in Power BI to ensure seamless Time Intelligence calculations (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATESINPERIOD`).
3. **Surrogate & Integer Key Indexing**: Natural keys are indexed, and integer date keys are supported for fast scanning.
4. **Column Storage Optimization**: High-cardinality descriptive columns reside exclusively in dimensions, keeping the fact table narrow and memory-compressed.
