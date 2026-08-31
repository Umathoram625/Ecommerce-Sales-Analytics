# Power BI DAX Measures Library

A comprehensive repository of 25+ production-grade DAX measures organized by analytical category.

---

## 1. Core Base Measures

```dax
// Total Revenue Generated
Total Sales = 
SUM(fact_sales[sales])
```

```dax
// Total Net Profit
Total Profit = 
SUM(fact_sales[profit])
```

```dax
// Overall Profit Margin %
Profit Margin % = 
DIVIDE([Total Profit], [Total Sales], 0)
```

```dax
// Total Units Sold
Total Quantity = 
SUM(fact_sales[quantity])
```

```dax
// Distinct Order Count
Total Orders = 
DISTINCTCOUNT(fact_sales[order_id])
```

```dax
// Average Order Value (AOV)
Average Order Value = 
DIVIDE([Total Sales], [Total Orders], 0)
```

```dax
// Total Estimated Cost
Total Cost = 
[Total Sales] - [Total Profit]
```

---

## 2. Time Intelligence & Growth Measures

```dax
// Year-To-Date (YTD) Revenue
Sales YTD = 
TOTALYTD([Total Sales], dim_dates[date])
```

```dax
// Prior Year (PY) Revenue
Sales Prior Year = 
CALCULATE(
    [Total Sales], 
    SAMEPERIODLASTYEAR(dim_dates[date])
)
```

```dax
// Year-over-Year (YoY) Sales Growth ($)
Sales YoY Growth $ = 
[Total Sales] - [Sales Prior Year]
```

```dax
// Year-over-Year (YoY) Sales Growth (%)
Sales YoY Growth % = 
DIVIDE([Sales YoY Growth $], [Sales Prior Year], 0)
```

```dax
// Year-To-Date (YTD) Profit
Profit YTD = 
TOTALYTD([Total Profit], dim_dates[date])
```

```dax
// Prior Year (PY) Profit
Profit Prior Year = 
CALCULATE(
    [Total Profit], 
    SAMEPERIODLASTYEAR(dim_dates[date])
)
```

```dax
// Year-over-Year (YoY) Profit Growth (%)
Profit YoY Growth % = 
DIVIDE([Total Profit] - [Profit Prior Year], [Profit Prior Year], 0)
```

```dax
// 3-Month Rolling Average Revenue
Sales 3M Rolling Avg = 
CALCULATE(
    AVERAGEX(
        DATESINPERIOD(dim_dates[date], LASTDATE(dim_dates[date]), -3, MONTH),
        [Total Sales]
    )
)
```

```dax
// Month-to-Date (MTD) Sales
Sales MTD = 
TOTALMTD([Total Sales], dim_dates[date])
```

---

## 3. Customer Analytics & Cohorts

```dax
// Unique Active Customers
Active Customers = 
DISTINCTCOUNT(fact_sales[customer_id])
```

```dax
// Average Revenue per Customer
Sales per Customer = 
DIVIDE([Total Sales], [Active Customers], 0)
```

```dax
// Repeat Customers (Customers with >1 order)
Repeat Customers Count = 
COUNTROWS(
    FILTER(
        VALUES(fact_sales[customer_id]),
        CALCULATE(DISTINCTCOUNT(fact_sales[order_id])) > 1
    )
)
```

```dax
// Repeat Customer Rate %
Repeat Customer Rate % = 
DIVIDE([Repeat Customers Count], [Active Customers], 0)
```

---

## 4. Pricing, Discounting & Margin Protection

```dax
// Weighted Average Discount Rate
Average Discount % = 
DIVIDE(
    SUMX(fact_sales, fact_sales[sales] * fact_sales[discount]),
    [Total Sales],
    0
)
```

```dax
// Revenue Generated from Deep Discount Transactions (>50%)
High Discount Sales = 
CALCULATE(
    [Total Sales],
    fact_sales[discount] > 0.50
)
```

```dax
// Cumulative Financial Loss from Loss-Making Orders
Total Unprofitable Loss = 
CALCULATE(
    SUM(fact_sales[profit]),
    fact_sales[profit] < 0
)
```

```dax
// Proportion of Transactions Operating at a Loss
Loss Making Transaction Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(fact_sales), fact_sales[profit] < 0),
    COUNTROWS(fact_sales),
    0
)
```

---

## 5. Shipping & Logistics Efficiency

```dax
// Average Transit Duration in Days
Avg Shipping Duration Days = 
AVERAGE(fact_sales[shipping_duration_days])
```

```dax
// Percentage of Orders with Transit Duration > 5 Days
Delayed Orders Rate % = 
DIVIDE(
    CALCULATE(DISTINCTCOUNT(fact_sales[order_id]), fact_sales[shipping_duration_days] > 5),
    [Total Orders],
    0
)
```
