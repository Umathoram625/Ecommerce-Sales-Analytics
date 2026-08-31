-- ==============================================================================
-- PROJECT: E-Commerce Sales & Profitability Analytics
-- FILE: 03_business_analysis_queries.sql
-- DESCRIPTION: Enterprise SQL Analysis Suite (22 Advanced Business Queries)
-- TECHNIQUES: CTEs, Window Functions (RANK, DENSE_RANK, LAG, LEAD, NTILE), 
--             Aggregations, Running Totals, Moving Averages, RFM Modeling, YoY Growth
-- COMPATIBILITY: Standard ANSI SQL (PostgreSQL, MySQL 8.0+, SQLite 3.30+, Snowflake)
-- ==============================================================================


-- ==============================================================================
-- SECTION 1: EXECUTIVE & OVERALL BUSINESS PERFORMANCE
-- ==============================================================================

-- QUERY 1: Executive KPI Summary
-- Business Question: What are the total revenue, gross profit, overall margin, total orders, total units sold, and Average Order Value (AOV)?
SELECT 
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM fact_sales;


-- QUERY 2: Annual Performance & Year-over-Year (YoY) Growth
-- Business Question: How has revenue and profit evolved each year, and what is the YoY percentage growth?
WITH yearly_metrics AS (
    SELECT 
        STRFTIME('%Y', order_date) AS order_year,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(DISTINCT order_id) AS total_orders
    FROM fact_sales
    GROUP BY STRFTIME('%Y', order_date)
)
SELECT 
    order_year,
    total_sales,
    LAG(total_sales, 1) OVER (ORDER BY order_year) AS prior_year_sales,
    ROUND(((total_sales - LAG(total_sales, 1) OVER (ORDER BY order_year)) / LAG(total_sales, 1) OVER (ORDER BY order_year)) * 100, 2) AS yoy_sales_growth_pct,
    total_profit,
    LAG(total_profit, 1) OVER (ORDER BY order_year) AS prior_year_profit,
    ROUND(((total_profit - LAG(total_profit, 1) OVER (ORDER BY order_year)) / LAG(total_profit, 1) OVER (ORDER BY order_year)) * 100, 2) AS yoy_profit_growth_pct,
    total_orders
FROM yearly_metrics
ORDER BY order_year;


-- QUERY 3: Monthly Sales Trend & 3-Month Moving Average
-- Business Question: What is the monthly sales trend and the smoothed 3-month rolling average to identify underlying momentum?
WITH monthly_sales AS (
    SELECT 
        STRFTIME('%Y-%m', order_date) AS year_month,
        ROUND(SUM(sales), 2) AS monthly_revenue,
        ROUND(SUM(profit), 2) AS monthly_profit
    FROM fact_sales
    GROUP BY STRFTIME('%Y-%m', order_date)
)
SELECT 
    year_month,
    monthly_revenue,
    monthly_profit,
    ROUND(AVG(monthly_revenue) OVER (ORDER BY year_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS rolling_3m_avg_revenue
FROM monthly_sales
ORDER BY year_month;


-- QUERY 4: Cumulative Running Total of Revenue & Profit
-- Business Question: What is the cumulative running total of revenue and profit across the entire business lifecycle?
WITH monthly_aggregates AS (
    SELECT 
        STRFTIME('%Y-%m', order_date) AS year_month,
        SUM(sales) AS sales,
        SUM(profit) AS profit
    FROM fact_sales
    GROUP BY STRFTIME('%Y-%m', order_date)
)
SELECT 
    year_month,
    ROUND(sales, 2) AS monthly_sales,
    ROUND(SUM(sales) OVER (ORDER BY year_month), 2) AS cumulative_sales,
    ROUND(profit, 2) AS monthly_profit,
    ROUND(SUM(profit) OVER (ORDER BY year_month), 2) AS cumulative_profit
FROM monthly_aggregates
ORDER BY year_month;


-- ==============================================================================
-- SECTION 2: PRODUCT & CATEGORY PROFITABILITY ANALYSIS
-- ==============================================================================

-- QUERY 5: Category & Sub-Category Performance Matrix
-- Business Question: What are the sales, profit, quantity, and profit margin for each sub-category within each major category?
SELECT 
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    SUM(f.quantity) AS units_sold,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category, p.sub_category
ORDER BY p.category, total_profit DESC;


-- QUERY 6: Sub-Category Revenue Contribution to Parent Category (Window SUM)
-- Business Question: What percentage does each sub-category contribute to its parent category's overall revenue?
WITH subcat_summary AS (
    SELECT 
        p.category,
        p.sub_category,
        SUM(f.sales) AS subcat_sales
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.category, p.sub_category
)
SELECT 
    category,
    sub_category,
    ROUND(subcat_sales, 2) AS subcat_sales,
    ROUND(SUM(subcat_sales) OVER (PARTITION BY category), 2) AS category_total_sales,
    ROUND((subcat_sales / SUM(subcat_sales) OVER (PARTITION BY category)) * 100, 2) AS category_share_pct
FROM subcat_summary
ORDER BY category, category_share_pct DESC;


-- QUERY 7: Top 10 Revenue Generating Products (DENSE_RANK)
-- Business Question: Which top 10 products generate the highest gross revenue?
WITH product_ranks AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.sub_category,
        ROUND(SUM(f.sales), 2) AS total_sales,
        ROUND(SUM(f.profit), 2) AS total_profit,
        DENSE_RANK() OVER (ORDER BY SUM(f.sales) DESC) AS revenue_rank
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.sub_category
)
SELECT * FROM product_ranks WHERE revenue_rank <= 10;


-- QUERY 8: Top 10 Most Unprofitable Products (Loss Leaders Analysis)
-- Business Question: Which products are generating the largest cumulative net financial losses?
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_loss,
    ROUND(AVG(f.discount) * 100, 1) AS avg_discount_pct,
    COUNT(f.row_id) AS transaction_count
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.sub_category
HAVING SUM(f.profit) < 0
ORDER BY total_loss ASC
LIMIT 10;


-- ==============================================================================
-- SECTION 3: PRICING, DISCOUNTING & MARGIN EROSION
-- ==============================================================================

-- QUERY 9: Profitability by Discount Tier
-- Business Question: How do different discount levels impact total sales, profit, and profit margins?
SELECT 
    discount_bracket,
    COUNT(row_id) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM fact_sales
GROUP BY discount_bracket
ORDER BY 
    CASE discount_bracket
        WHEN 'No Discount (0%)' THEN 1
        WHEN 'Low Discount (1-20%)' THEN 2
        WHEN 'Medium Discount (21-50%)' THEN 3
        WHEN 'High Discount (>50%)' THEN 4
        ELSE 5
    END;


-- QUERY 10: Deep Discount Outlier Audit (>50% Discount Impact)
-- Business Question: What is the financial damage caused by deep discounting (>50%) across product categories?
SELECT 
    p.category,
    COUNT(f.row_id) AS deep_discount_orders,
    ROUND(SUM(f.sales), 2) AS deep_discount_sales,
    ROUND(SUM(f.profit), 2) AS total_loss_incurred,
    ROUND(AVG(f.discount) * 100, 1) AS avg_discount_given
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE f.discount > 0.50
GROUP BY p.category
ORDER BY total_loss_incurred ASC;


-- ==============================================================================
-- SECTION 4: GEOGRAPHIC & REGIONAL PERFORMANCE
-- ==============================================================================

-- QUERY 11: Regional Performance & Profit Contribution Ranking
-- Business Question: How does each geographic region rank in terms of sales volume and bottom-line profit?
SELECT 
    g.region,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT f.order_id) AS order_count,
    DENSE_RANK() OVER (ORDER BY SUM(f.profit) DESC) AS profit_rank
FROM fact_sales f
JOIN dim_geography g ON f.postal_code = g.postal_code
GROUP BY g.region
ORDER BY profit_rank;


-- QUERY 12: Bottom 10 Loss-Making States
-- Business Question: Which states are operating at a net loss and what are their average discount rates?
SELECT 
    g.state,
    g.region,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS net_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(f.discount) * 100, 1) AS avg_discount_pct,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_geography g ON f.postal_code = g.postal_code
GROUP BY g.state, g.region
HAVING SUM(f.profit) < 0
ORDER BY net_profit ASC
LIMIT 10;


-- QUERY 13: Top 10 High-Performing Cities by Net Profit
-- Business Question: What are the top 10 most profitable metropolitan markets?
SELECT 
    g.city,
    g.state,
    g.region,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS margin_pct,
    COUNT(DISTINCT f.order_id) AS order_count
FROM fact_sales f
JOIN dim_geography g ON f.postal_code = g.postal_code
GROUP BY g.city, g.state, g.region
ORDER BY total_profit DESC
LIMIT 10;


-- ==============================================================================
-- SECTION 5: CUSTOMER BEHAVIOR & RFM SEGMENTATION
-- ==============================================================================

-- QUERY 14: Customer Lifetime Value (CLV) & Top Spenders
-- Business Question: Who are the top 15 highest-value customers across their lifetime with the business?
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_units_bought,
    ROUND(SUM(f.sales), 2) AS lifetime_spend,
    ROUND(SUM(f.profit), 2) AS lifetime_profit,
    ROUND(SUM(f.sales) / COUNT(DISTINCT f.order_id), 2) AS avg_order_value
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY lifetime_spend DESC
LIMIT 15;


-- QUERY 15: Pure SQL RFM Scoring (Recency, Frequency, Monetary with NTILE)
-- Business Question: How can we compute RFM scores (1 to 5) directly inside SQL using NTILE window functions?
WITH customer_rfm_raw AS (
    SELECT 
        customer_id,
        JULIANDAY((SELECT MAX(order_date) FROM fact_sales)) - JULIANDAY(MAX(order_date)) AS recency_days,
        COUNT(DISTINCT order_id) AS frequency_orders,
        SUM(sales) AS monetary_value
    FROM fact_sales
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency_orders,
        monetary_value,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM customer_rfm_raw
)
SELECT 
    customer_id,
    ROUND(recency_days, 0) AS recency_days,
    frequency_orders,
    ROUND(monetary_value, 2) AS monetary_value,
    r_score,
    f_score,
    m_score,
    (r_score || f_score || m_score) AS rfm_cell
FROM rfm_scores
ORDER BY monetary_value DESC
LIMIT 15;


-- QUERY 16: Pareto Analysis (80/20 Rule on Customer Base)
-- Business Question: What percentage of total company revenue is generated by the top 20% of customers?
WITH customer_spend AS (
    SELECT 
        customer_id,
        SUM(sales) AS total_spend
    FROM fact_sales
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT 
        customer_id,
        total_spend,
        ROW_NUMBER() OVER (ORDER BY total_spend DESC) AS customer_rank,
        COUNT(*) OVER () AS total_customer_count,
        SUM(total_spend) OVER (ORDER BY total_spend DESC) AS cumulative_spend,
        SUM(total_spend) OVER () AS total_company_revenue
    FROM customer_spend
)
SELECT 
    customer_rank,
    ROUND((CAST(customer_rank AS FLOAT) / total_customer_count) * 100, 2) AS customer_percentile,
    ROUND(total_spend, 2) AS customer_spend,
    ROUND((cumulative_spend / total_company_revenue) * 100, 2) AS cumulative_revenue_pct
FROM ranked_customers
WHERE customer_rank IN (
    CAST(total_customer_count * 0.10 AS INT),
    CAST(total_customer_count * 0.20 AS INT),
    CAST(total_customer_count * 0.50 AS INT),
    CAST(total_customer_count * 0.80 AS INT),
    total_customer_count
)
ORDER BY customer_rank;


-- QUERY 17: Customer Segment Performance (Consumer vs Corporate vs Home Office)
-- Business Question: How does revenue, profit margin, and AOV differ across primary customer segments?
SELECT 
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.sales), 2) AS total_revenue,
    ROUND(SUM(f.profit), 2) AS total_profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(f.sales) / COUNT(DISTINCT f.order_id), 2) AS average_order_value
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY total_revenue DESC;


-- QUERY 18: Customer Cohort Retention & Repeat Purchase Rate
-- Business Question: How many customers are single-order purchasers versus repeat buyers?
WITH customer_order_counts AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_sales
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN order_count = 1 THEN '1 Order (One-Time Buyer)'
        WHEN order_count BETWEEN 2 AND 4 THEN '2-4 Orders (Occasional)'
        WHEN order_count BETWEEN 5 AND 9 THEN '5-9 Orders (Frequent)'
        ELSE '10+ Orders (Power Buyer)'
    END AS buyer_cohort,
    COUNT(customer_id) AS customer_count,
    ROUND((CAST(COUNT(customer_id) AS FLOAT) / (SELECT COUNT(*) FROM customer_order_counts)) * 100, 2) AS pct_of_customers
FROM customer_order_counts
GROUP BY buyer_cohort
ORDER BY customer_count DESC;


-- ==============================================================================
-- SECTION 6: SHIPPING & LOGISTICS EFFICIENCY
-- ==============================================================================

-- QUERY 19: Shipping Duration & Profitability by Ship Mode
-- Business Question: What is the average transit duration, sales volume, and margin across shipping modes?
SELECT 
    ship_mode,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(AVG(shipping_duration_days), 2) AS avg_shipping_days,
    MIN(shipping_duration_days) AS min_shipping_days,
    MAX(shipping_duration_days) AS max_shipping_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM fact_sales
GROUP BY ship_mode
ORDER BY avg_shipping_days ASC;


-- QUERY 20: Delivery Delay Identification (>5 Days In Transit)
-- Business Question: What proportion of standard class shipments experience fulfillment delays exceeding 5 days?
SELECT 
    ship_mode,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN shipping_duration_days > 5 THEN 1 ELSE 0 END) AS delayed_orders_gt_5d,
    ROUND((CAST(SUM(CASE WHEN shipping_duration_days > 5 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT order_id)) * 100, 2) AS pct_delayed
FROM fact_sales
GROUP BY ship_mode
ORDER BY pct_delayed DESC;


-- ==============================================================================
-- SECTION 7: ADVANCED BASKET & CROSS-SELLING ANALYSIS
-- ==============================================================================

-- QUERY 21: Cross-Selling / Frequently Bought Together Sub-Categories
-- Business Question: Which pairs of product sub-categories are most frequently purchased together within the same order?
WITH order_subcats AS (
    SELECT DISTINCT 
        f.order_id,
        p.sub_category
    FROM fact_sales f
    JOIN dim_products p ON f.product_id = p.product_id
)
SELECT 
    a.sub_category AS subcat_a,
    b.sub_category AS subcat_b,
    COUNT(DISTINCT a.order_id) AS times_bought_together
FROM order_subcats a
JOIN order_subcats b ON a.order_id = b.order_id AND a.sub_category < b.sub_category
GROUP BY a.sub_category, b.sub_category
ORDER BY times_bought_together DESC
LIMIT 10;


-- QUERY 22: First-Time Purchase Acquisition Cohort Analysis
-- Business Question: Which year did each customer first purchase, and what is the cumulative revenue generated by each cohort?
WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        MIN(STRFTIME('%Y', order_date)) AS cohort_year
    FROM fact_sales
    GROUP BY customer_id
)
SELECT 
    c.cohort_year,
    COUNT(DISTINCT c.customer_id) AS new_customers_acquired,
    ROUND(SUM(f.sales), 2) AS total_cohort_revenue,
    ROUND(SUM(f.profit), 2) AS total_cohort_profit,
    ROUND(SUM(f.sales) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_acquired_customer
FROM customer_first_purchase c
JOIN fact_sales f ON c.customer_id = f.customer_id
GROUP BY c.cohort_year
ORDER BY c.cohort_year ASC;
