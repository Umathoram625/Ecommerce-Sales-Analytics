-- ==============================================================================
-- PROJECT: E-Commerce Sales Analytics
-- FILE: 01_schema_setup.sql
-- DESCRIPTION: Database DDL definitions for Star Schema & Staging tables
-- COMPATIBILITY: MySQL 8.0+, PostgreSQL 13+, SQLite 3.30+
-- ==============================================================================

-- Create Dimension: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL
);

-- Create Dimension: Products
CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(30) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL
);

-- Create Dimension: Geography
CREATE TABLE IF NOT EXISTS dim_geography (
    postal_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Create Dimension: Dates (Calendar)
CREATE TABLE IF NOT EXISTS dim_dates (
    date DATE PRIMARY KEY,
    date_id INT NOT NULL,
    year INT NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend INT NOT NULL
);

-- Create Fact: Sales Transactions
CREATE TABLE IF NOT EXISTS fact_sales (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(50) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    sales DECIMAL(12, 4) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(6, 4) NOT NULL,
    profit DECIMAL(12, 4) NOT NULL,
    shipping_duration_days INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    profit_margin_pct DECIMAL(8, 2) NOT NULL,
    is_profitable INT NOT NULL,
    discount_bracket VARCHAR(30) NOT NULL
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_sales_order_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_product ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_postal ON fact_sales(postal_code);
