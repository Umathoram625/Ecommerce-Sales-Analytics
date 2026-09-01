# ==============================================================================
# SCRIPT: clean_data.py
# PROJECT: E-Commerce Sales Analytics
# DESCRIPTION: Production data cleaning & validation pipeline
# ==============================================================================

import pandas as pd
import numpy as np
import os

def clean_ecommerce_data(raw_filepath: str, output_filepath: str):
    print(f"Loading raw dataset from: {raw_filepath}")
    df_raw = pd.read_csv(raw_filepath, encoding='windows-1252')
    initial_row_count = len(df_raw)
    initial_col_count = len(df_raw.columns)
    print(f"Initial Shape: {initial_row_count:,} rows, {initial_col_count} columns")
    
    # Work on an isolated copy
    df = df_raw.copy()
    
    # 1. Standardize column names to lower_snake_case
    df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # 2. Date parsing
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed')
    df['ship_date'] = pd.to_datetime(df['ship_date'], format='mixed')
    
    # 3. Postal Code handling (preserve as string with 5-digit zero padding)
    df['postal_code'] = df['postal_code'].astype(str).str.zfill(5)
    
    # 4. Duplicate checks
    exact_duplicates = df.duplicated().sum()
    if exact_duplicates > 0:
        df = df.drop_duplicates().reset_index(drop=True)
    print(f"Exact duplicates removed: {exact_duplicates}")
    
    # 5. Missing values check
    missing_count = df.isnull().sum().sum()
    print(f"Total missing values: {missing_count}")
    
    # 6. Feature Engineering (Analytical Columns)
    df['year'] = df['order_date'].dt.year
    df['month_number'] = df['order_date'].dt.month
    df['month'] = df['order_date'].dt.strftime('%B')
    df['quarter'] = 'Q' + df['order_date'].dt.quarter.astype(str)
    # Formatted as YYYY-MM so it sorts chronologically and alphabetically
    df['year_month'] = df['order_date'].dt.strftime('%Y-%m')
    df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
    df['profit_margin'] = (df['profit'] / df['sales']).round(4)
    
    # 7. Validation of numerical boundaries
    assert (df['sales'] > 0).all(), "Error: Found non-positive sales values"
    assert (df['quantity'] >= 1).all(), "Error: Found quantity < 1"
    assert (df['discount'] >= 0.0).all() and (df['discount'] <= 1.0).all(), "Error: Found discounts outside [0, 1]"
    assert (df['shipping_days'] >= 0).all(), "Error: Found ship_date < order_date"
    
    final_row_count = len(df)
    final_col_count = len(df.columns)
    print(f"Final Cleaned Shape: {final_row_count:,} rows, {final_col_count} columns")
    
    # Save master cleaned dataset
    df.to_csv(output_filepath, index=False)
    print(f"Cleaned dataset successfully saved to: {output_filepath}")
    return df

if __name__ == '__main__':
    raw_path = os.path.join('data', 'raw', 'Sample_Superstore.csv')
    cleaned_path = os.path.join('data', 'cleaned', 'superstore_cleaned.csv')
    clean_ecommerce_data(raw_path, cleaned_path)
