# Power BI DAX Measures Library & Technical Reference

A complete repository of 28 production-grade DAX measures designed for the E-Commerce Sales Analytics model, organized into logical measure tables.

---

## 1. Core Base Commercial Measures

```dax
// Measure 01: Total Gross Sales
Total Sales = 
SUM(FactSales[sales])
```
* **Description**: Sum of gross revenue across all transaction line items.
* **Reconciled Value**: `$2,297,200.86`

```dax
// Measure 02: Total Net Profit
Total Profit = 
SUM(FactSales[profit])
```
* **Description**: Cumulative bottom-line net profit generated.
* **Reconciled Value**: `$286,397.02`

```dax
// Measure 03: Overall Profit Margin %
Profit Margin % = 
DIVIDE([Total Profit], [Total Sales], 0)
```
* **Description**: Gross commercial profit margin expressed as a percentage.
* **Reconciled Value**: `12.47%`

```dax
// Measure 04: Total Quantity Sold
Total Quantity = 
SUM(FactSales[quantity])
```
* **Description**: Total number of physical units fulfilled.
* **Reconciled Value**: `37,873 units`

```dax
// Measure 05: Total Orders
Total Orders = 
DISTINCTCOUNT(FactSales[order_id])
```
* **Description**: Count of distinct customer purchase orders.
* **Reconciled Value**: `5,009 orders`

```dax
// Measure 06: Total Customers
Total Customers = 
DISTINCTCOUNT(FactSales[customer_id])
```
* **Description**: Total unique purchasing client accounts.
* **Reconciled Value**: `793 accounts`

```dax
// Measure 07: Average Order Value (AOV)
Average Order Value = 
DIVIDE([Total Sales], [Total Orders], 0)
```
* **Description**: Average gross spend per completed transaction order.
* **Reconciled Value**: `$458.61`

```dax
// Measure 08: Average Discount Rate %
Average Discount % = 
AVERAGE(FactSales[discount])
```
* **Description**: Arithmetic mean discount applied across order lines.
* **Reconciled Value**: `15.62%`

```dax
// Measure 09: Average Shipping Duration
Avg Shipping Days = 
AVERAGE(FactSales[shipping_days])
```
* **Description**: Mean transit duration in calendar days from order placement to shipment.
* **Reconciled Value**: `3.96 days`

---

## 2. Time Intelligence & Growth Measures

```dax
// Measure 10: Year-to-Date (YTD) Revenue
Sales YTD = 
TOTALYTD([Total Sales], DimDate[date])
```

```dax
// Measure 11: Prior Year (Last Year) Revenue
Sales LY = 
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(DimDate[date])
)
```

```dax
// Measure 12: Year-over-Year (YoY) Sales Growth %
Sales YoY % = 
DIVIDE([Total Sales] - [Sales LY], [Sales LY], 0)
```

```dax
// Measure 13: Year-to-Date (YTD) Net Profit
Profit YTD = 
TOTALYTD([Total Profit], DimDate[date])
```

```dax
// Measure 14: Prior Year Net Profit
Profit LY = 
CALCULATE(
    [Total Profit],
    SAMEPERIODLASTYEAR(DimDate[date])
)
```

```dax
// Measure 15: Year-over-Year (YoY) Profit Growth %
Profit YoY % = 
DIVIDE([Total Profit] - [Profit LY], [Profit LY], 0)
```

```dax
// Measure 16: 3-Month Rolling Average Revenue
Sales 3M Rolling Avg = 
CALCULATE(
    AVERAGEX(
        DATESINPERIOD(DimDate[date], LASTDATE(DimDate[date]), -3, MONTH),
        [Total Sales]
    )
)
```

---

## 3. Customer & RFM Intelligence Measures

```dax
// Measure 17: Average Revenue per Customer
Sales per Customer = 
DIVIDE([Total Sales], [Total Customers], 0)
```
* **Reconciled Value**: `$2,896.85`

```dax
// Measure 18: Repeat Customer Count (>1 Order)
Repeat Customers Count = 
COUNTROWS(
    FILTER(
        VALUES(FactSales[customer_id]),
        CALCULATE(DISTINCTCOUNT(FactSales[order_id])) > 1
    )
)
```
* **Reconciled Value**: `780 accounts`

```dax
// Measure 19: Repeat Customer Rate %
Repeat Customer % = 
DIVIDE([Repeat Customers Count], [Total Customers], 0)
```
* **Reconciled Value**: `98.36%`

```dax
// Measure 20: Champions Segment Revenue
Champions Sales = 
CALCULATE(
    [Total Sales],
    DimCustomer[rfm_segment] = "Champions"
)
```
* **Reconciled Value**: `$560,498.82 (24.40%)`

```dax
// Measure 21: At-Risk Segment Revenue
At Risk Sales = 
CALCULATE(
    [Total Sales],
    DimCustomer[rfm_segment] = "At Risk"
)
```
* **Reconciled Value**: `$445,804.88 (19.41%)`

```dax
// Measure 22: At-Risk Segment Profit
At Risk Profit = 
CALCULATE(
    [Total Profit],
    DimCustomer[rfm_segment] = "At Risk"
)
```
* **Reconciled Value**: `$72,315.11 (25.25%)`

---

## 4. Profitability & Pricing Risk Measures

```dax
// Measure 23: Loss-Making Order Sales Volume
Loss-Making Sales = 
CALCULATE(
    [Total Sales],
    FactSales[profit] < 0
)
```
* **Reconciled Value**: `$468,707.15 (20.40% of sales)`

```dax
// Measure 24: Total Financial Loss Amount
Total Unprofitable Loss = 
CALCULATE(
    SUM(FactSales[profit]),
    FactSales[profit] < 0
)
```
* **Reconciled Value**: `-$156,131.29`

```dax
// Measure 25: Loss-Making Order Line Rate %
Loss Order Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(FactSales), FactSales[profit] < 0),
    COUNTROWS(FactSales),
    0
)
```
* **Reconciled Value**: `18.72% (1,871 / 9,994)`

```dax
// Measure 26: Heavy Discount Sales Volume (>20% Discount)
Heavy Discount Sales = 
CALCULATE(
    [Total Sales],
    FactSales[discount] > 0.20
)
```
* **Reconciled Value**: `$390,268.49`

---

## 5. Ranking & Shipping Logistics Measures

```dax
// Measure 27: Top Product Revenue Contribution
Top Product Sales = 
MAXX(
    VALUES(DimProduct[product_name]),
    [Total Sales]
)
```

```dax
// Measure 28: Shipments Delivered under SLA Target
On-Time Shipment Rate % = 
DIVIDE(
    CALCULATE(
        COUNTROWS(FactSales),
        RELATED(DimShipping[sla_target_days]) >= FactSales[shipping_days]
    ),
    COUNTROWS(FactSales),
    0
)
```
