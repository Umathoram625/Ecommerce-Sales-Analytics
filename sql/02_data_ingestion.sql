-- ==============================================================================
-- PROJECT: E-Commerce Sales Analytics
-- FILE: 02_data_ingestion.sql
-- DESCRIPTION: Data loading procedures and bulk import commands
-- ==============================================================================

-- Example 1: MySQL LOAD DATA INFILE
/*
LOAD DATA LOCAL INFILE 'data/cleaned/dim_customers.csv'
INTO TABLE dim_customers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '
'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/cleaned/dim_products.csv'
INTO TABLE dim_products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '
'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/cleaned/dim_geography.csv'
INTO TABLE dim_geography
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '
'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/cleaned/dim_dates.csv'
INTO TABLE dim_dates
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '
'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'data/cleaned/fact_sales.csv'
INTO TABLE fact_sales
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '
'
IGNORE 1 ROWS;
*/

-- Example 2: PostgreSQL COPY Command
/*
\copy dim_customers FROM 'data/cleaned/dim_customers.csv' WITH (FORMAT csv, HEADER true);
\copy dim_products FROM 'data/cleaned/dim_products.csv' WITH (FORMAT csv, HEADER true);
\copy dim_geography FROM 'data/cleaned/dim_geography.csv' WITH (FORMAT csv, HEADER true);
\copy dim_dates FROM 'data/cleaned/dim_dates.csv' WITH (FORMAT csv, HEADER true);
\copy fact_sales FROM 'data/cleaned/fact_sales.csv' WITH (FORMAT csv, HEADER true);
*/
