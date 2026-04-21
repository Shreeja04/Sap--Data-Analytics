"""
=============================================================
  End-to-End Order-to-Cash (O2C) Analytics System
  Data Processing Script
  Author: Shreeja Ghosh | Roll No.: 2330048
=============================================================
  This script:
    1. Loads all raw CSV datasets
    2. Cleans the data (handles missing values, fixes date formats)
    3. Merges all datasets into one master dataset
    4. Calculates KPIs (Key Performance Indicators)
    5. Saves the final processed dataset
    6. Performs advanced analytics (Risk Scoring, Trend Analysis)
=============================================================
"""

# -------------------------------------------------------
# STEP 0: Import Required Libraries
# -------------------------------------------------------
# pandas  --> for working with tables of data
# numpy   --> for math operations
# os      --> for working with files/folders
# datetime --> for working with dates

import pandas as pd
import numpy as np
import os
from datetime import datetime

print("="*60)
print("  O2C Analytics System - Data Processing Started")
print("="*60)

# -------------------------------------------------------
# STEP 1: Set File Paths
# -------------------------------------------------------
# We tell Python WHERE to find our CSV files.
# os.path.join builds the correct file path for any OS.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder of this script
RAW_DIR  = os.path.join(BASE_DIR, '..', 'data', 'raw')        # raw data folder
PROC_DIR = os.path.join(BASE_DIR, '..', 'data', 'processed')  # output folder

# Create the processed folder if it doesn't exist yet
os.makedirs(PROC_DIR, exist_ok=True)

print("\n[1/7] File paths set successfully.")

# -------------------------------------------------------
# STEP 2: Load Raw CSV Files
# -------------------------------------------------------
# pd.read_csv() reads a CSV file and stores it as a DataFrame.
# A DataFrame is like an Excel table in Python.

try:
    customers   = pd.read_csv(os.path.join(RAW_DIR, 'customers.csv'))
    orders      = pd.read_csv(os.path.join(RAW_DIR, 'sales_orders.csv'))
    deliveries  = pd.read_csv(os.path.join(RAW_DIR, 'deliveries.csv'))
    invoices    = pd.read_csv(os.path.join(RAW_DIR, 'invoices.csv'))
    payments    = pd.read_csv(os.path.join(RAW_DIR, 'payments.csv'))
    print("[2/7] All datasets loaded successfully.")
except FileNotFoundError as e:
    print(f"ERROR: Could not find file - {e}")
    print("Make sure you run this script from the 'scripts' folder.")
    exit()

# Quick check: print how many rows each table has
print(f"      Customers  : {len(customers)} rows")
print(f"      Orders     : {len(orders)} rows")
print(f"      Deliveries : {len(deliveries)} rows")
print(f"      Invoices   : {len(invoices)} rows")
print(f"      Payments   : {len(payments)} rows")

# -------------------------------------------------------
# STEP 3: Clean the Data
# -------------------------------------------------------
# pd.to_datetime() converts text like "2024-01-05" into a real date Python understands.
# errors='coerce' means: if a date is invalid, put NaT (Not a Time) instead of crashing.

print("\n[3/7] Cleaning data...")

# -- Customers --
customers['CustomerSince'] = pd.to_datetime(customers['CustomerSince'], errors='coerce')
customers['CustomerName']  = customers['CustomerName'].str.strip()   # remove extra spaces
customers['Region']        = customers['Region'].str.strip()

# -- Orders --
orders['OrderDate']            = pd.to_datetime(orders['OrderDate'], errors='coerce')
orders['ExpectedDeliveryDate'] = pd.to_datetime(orders['ExpectedDeliveryDate'], errors='coerce')
orders['TotalOrderValue']      = pd.to_numeric(orders['TotalOrderValue'], errors='coerce')  # ensure numbers

# -- Deliveries --
deliveries['PlannedDeliveryDate'] = pd.to_datetime(deliveries['PlannedDeliveryDate'], errors='coerce')
deliveries['ActualDeliveryDate']  = pd.to_datetime(deliveries['ActualDeliveryDate'], errors='coerce')
deliveries['ShippingCost']        = pd.to_numeric(deliveries['ShippingCost'], errors='coerce')

# -- Invoices --
invoices['InvoiceDate']       = pd.to_datetime(invoices['InvoiceDate'], errors='coerce')
invoices['InvoiceDueDate']    = pd.to_datetime(invoices['InvoiceDueDate'], errors='coerce')
invoices['TotalInvoiceAmount']= pd.to_numeric(invoices['TotalInvoiceAmount'], errors='coerce')

# -- Payments --
payments['PaymentDate']       = pd.to_datetime(payments['PaymentDate'], errors='coerce')
payments['PaymentAmount']     = pd.to_numeric(payments['PaymentAmount'], errors='coerce')
payments['DaysToPayFromInvoice'] = pd.to_numeric(payments['DaysToPayFromInvoice'], errors='coerce')

# Check for missing values (NaN) in key columns
print("      Checking for missing values:")
for df, name in [(customers,'Customers'),(orders,'Orders'),(deliveries,'Deliveries'),
                 (invoices,'Invoices'),(payments,'Payments')]:
    missing = df.isnull().sum().sum()   # total missing values in entire table
    print(f"      {name}: {missing} missing value(s)")

print("      Data cleaning complete.")

# -------------------------------------------------------
# STEP 4: Merge All Datasets into ONE Master Table
# -------------------------------------------------------
# We join tables using common "key" columns, just like SQL JOINs.
# how='left' means: keep all rows from the LEFT table, match what you can from the right.

print("\n[4/7] Merging datasets into master table...")

# Step 4a: Merge Orders + Customers (join on CustomerID)
master = pd.merge(orders, customers[['CustomerID','CustomerName','Region',
                                      'CustomerSegment','PaymentTerms','CreditLimit']],
                  on='CustomerID', how='left')

# Step 4b: Add Delivery information (join on OrderID)
master = pd.merge(master, deliveries[['OrderID','DeliveryID','PlannedDeliveryDate',
                                       'ActualDeliveryDate','DeliveryStatus',
                                       'LogisticsPartner','ShippingCost']],
                  on='OrderID', how='left')

# Step 4c: Add Invoice information (join on OrderID)
master = pd.merge(master, invoices[['OrderID','InvoiceID','InvoiceDate',
                                     'InvoiceDueDate','TotalInvoiceAmount','InvoiceStatus']],
                  on='OrderID', how='left')

# Step 4d: Add Payment information (join on InvoiceID)
master = pd.merge(master, payments[['InvoiceID','PaymentID','PaymentDate',
                                     'PaymentAmount','PaymentMethod',
                                     'DaysToPayFromInvoice','LateFeeApplied']],
                  on='InvoiceID', how='left')

print(f"      Master dataset created: {len(master)} rows, {len(master.columns)} columns")

# -------------------------------------------------------
# STEP 5: Calculate KPIs (Key Performance Indicators)
# -------------------------------------------------------
# These are business metrics that tell us HOW WELL things are going.

print("\n[5/7] Calculating KPIs...")

# KPI 1: Delivery Delay (in days)
# Formula: ActualDeliveryDate - PlannedDeliveryDate
# Positive = late delivery, Negative = early delivery, 0 = on time
master['DeliveryDelayDays'] = (
    master['ActualDeliveryDate'] - master['PlannedDeliveryDate']
).dt.days
# .dt.days extracts the number of days from a time difference

# KPI 2: Payment Delay (in days)
# Formula: PaymentDate - InvoiceDueDate
# Positive = paid late, Negative = paid early
master['PaymentDelayDays'] = (
    master['PaymentDate'] - master['InvoiceDueDate']
).dt.days

# KPI 3: Order-to-Cash Cycle Time (total days from order to payment)
# Formula: PaymentDate - OrderDate
# This is THE most important O2C metric
master['O2C_CycleTimeDays'] = (
    master['PaymentDate'] - master['OrderDate']
).dt.days

# KPI 4: Invoice-to-Payment Days (how fast customers pay after invoice)
master['InvoiceToPaymentDays'] = (
    master['PaymentDate'] - master['InvoiceDate']
).dt.days

# KPI 5: Is Delivery Late? (Yes/No flag)
# np.where(condition, value_if_true, value_if_false)
master['IsDeliveryLate'] = np.where(master['DeliveryDelayDays'] > 0, 'Yes', 'No')

# KPI 6: Is Payment Late? (Was the invoice paid after due date?)
master['IsPaymentLate'] = np.where(master['PaymentDelayDays'] > 0, 'Yes', 'No')

# KPI 7: Order Month and Quarter (for trend analysis)
master['OrderMonth']   = master['OrderDate'].dt.to_period('M').astype(str)
master['OrderQuarter'] = master['OrderDate'].dt.to_period('Q').astype(str)
master['OrderYear']    = master['OrderDate'].dt.year

print("      KPIs calculated:")
print(f"      Avg Delivery Delay   : {master['DeliveryDelayDays'].mean():.1f} days")
print(f"      Avg Payment Delay    : {master['PaymentDelayDays'].mean():.1f} days")
print(f"      Avg O2C Cycle Time   : {master['O2C_CycleTimeDays'].mean():.1f} days")
print(f"      Late Deliveries      : {(master['IsDeliveryLate']=='Yes').sum()} orders")
print(f"      Late Payments        : {(master['IsPaymentLate']=='Yes').sum()} orders")

# -------------------------------------------------------
# STEP 6: Advanced Analytics - Customer Risk Scoring
# -------------------------------------------------------
# We assign each customer a RISK SCORE (Low / Medium / High)
# based on their payment behavior.
# Higher score = more risky customer (pays late often)

print("\n[6/7] Running Advanced Analytics - Customer Risk Scoring...")

# Calculate per-customer metrics
customer_metrics = master.groupby('CustomerID').agg(
    TotalOrders        = ('OrderID',          'count'),          # how many orders
    TotalRevenue       = ('TotalOrderValue',   'sum'),            # total money
    AvgPaymentDelay    = ('PaymentDelayDays',  'mean'),           # avg days late
    AvgDeliveryDelay   = ('DeliveryDelayDays', 'mean'),           # avg delivery delay
    LatePaymentCount   = ('IsPaymentLate',     lambda x: (x=='Yes').sum()),  # count of late payments
    LateDeliveryCount  = ('IsDeliveryLate',    lambda x: (x=='Yes').sum()),
).reset_index()
# .reset_index() turns the groupby result back into a normal table

# Risk Score Logic:
# Points: +2 if avg payment delay > 30 days
#         +1 if avg payment delay > 0 days
#         +1 if more than 1 late payment
#         +1 if avg delivery delay > 5 days

def calculate_risk_score(row):
    """Assigns a numeric risk score to each customer row."""
    score = 0
    if row['AvgPaymentDelay'] > 30:
        score += 2   # very late payer
    elif row['AvgPaymentDelay'] > 0:
        score += 1   # somewhat late payer
    if row['LatePaymentCount'] > 1:
        score += 1   # multiple late payments
    if row['AvgDeliveryDelay'] > 5:
        score += 1   # deliveries often late (supply chain issue)
    return score

customer_metrics['RiskScore']    = customer_metrics.apply(calculate_risk_score, axis=1)
# axis=1 means apply the function row by row

# Convert score to Risk Category
def score_to_category(score):
    if score >= 3:
        return 'High Risk'
    elif score >= 1:
        return 'Medium Risk'
    else:
        return 'Low Risk'

customer_metrics['RiskCategory'] = customer_metrics['RiskScore'].apply(score_to_category)

# Merge risk scores back into master dataset
master = pd.merge(master, customer_metrics[['CustomerID','RiskScore','RiskCategory',
                                             'TotalOrders','LatePaymentCount']],
                  on='CustomerID', how='left')

print("      Risk Score Distribution:")
print(customer_metrics['RiskCategory'].value_counts().to_string())

# -------------------------------------------------------
# STEP 7: Revenue Trend Analysis
# -------------------------------------------------------
monthly_revenue = master.groupby('OrderMonth').agg(
    MonthlyRevenue = ('TotalOrderValue', 'sum'),
    OrderCount     = ('OrderID',         'count')
).reset_index()

monthly_revenue['RevenueGrowth_pct'] = monthly_revenue['MonthlyRevenue'].pct_change() * 100
# pct_change() calculates % change from one row to the next

print("\n      Monthly Revenue Trend:")
print(monthly_revenue[['OrderMonth','MonthlyRevenue','OrderCount','RevenueGrowth_pct']].to_string(index=False))

# -------------------------------------------------------
# STEP 8: Save All Output Files
# -------------------------------------------------------
print("\n[7/7] Saving output files...")

# Save master dataset
master_path = os.path.join(PROC_DIR, 'o2c_master_dataset.csv')
master.to_csv(master_path, index=False)
print(f"      Saved: o2c_master_dataset.csv ({len(master)} rows)")

# Save customer risk scores
risk_path = os.path.join(PROC_DIR, 'customer_risk_scores.csv')
# Add customer names for readability
risk_with_names = pd.merge(customer_metrics,
                           customers[['CustomerID','CustomerName','Region','CustomerSegment']],
                           on='CustomerID', how='left')
risk_with_names.to_csv(risk_path, index=False)
print(f"      Saved: customer_risk_scores.csv ({len(risk_with_names)} rows)")

# Save monthly revenue trends
trend_path = os.path.join(PROC_DIR, 'monthly_revenue_trend.csv')
monthly_revenue.to_csv(trend_path, index=False)
print(f"      Saved: monthly_revenue_trend.csv")

# Save KPI Summary
kpi_summary = {
    'KPI': [
        'Total Revenue (INR)',
        'Total Orders',
        'Avg O2C Cycle Time (Days)',
        'Avg Delivery Delay (Days)',
        'Avg Payment Delay (Days)',
        'Late Delivery Rate (%)',
        'Late Payment Rate (%)',
        'High Risk Customers',
        'Total Invoice Value (INR)'
    ],
    'Value': [
        master['TotalOrderValue'].sum(),
        len(master),
        round(master['O2C_CycleTimeDays'].mean(), 1),
        round(master['DeliveryDelayDays'].mean(), 1),
        round(master['PaymentDelayDays'].mean(), 1),
        round((master['IsDeliveryLate']=='Yes').mean() * 100, 1),
        round((master['IsPaymentLate']=='Yes').mean() * 100, 1),
        (customer_metrics['RiskCategory']=='High Risk').sum(),
        master['TotalInvoiceAmount'].sum()
    ]
}
kpi_df = pd.DataFrame(kpi_summary)
kpi_path = os.path.join(PROC_DIR, 'kpi_summary.csv')
kpi_df.to_csv(kpi_path, index=False)
print(f"      Saved: kpi_summary.csv")

# -------------------------------------------------------
# FINAL: Print Summary Report
# -------------------------------------------------------
print("\n" + "="*60)
print("  PROCESSING COMPLETE - KPI SUMMARY REPORT")
print("="*60)
print(f"  Total Revenue        : INR {master['TotalOrderValue'].sum():,.0f}")
print(f"  Total Orders         : {len(master)}")
print(f"  Total Customers      : {master['CustomerID'].nunique()}")
print(f"  Avg O2C Cycle Time   : {master['O2C_CycleTimeDays'].mean():.1f} days")
print(f"  Avg Delivery Delay   : {master['DeliveryDelayDays'].mean():.1f} days")
print(f"  Late Delivery Rate   : {(master['IsDeliveryLate']=='Yes').mean()*100:.1f}%")
print(f"  Late Payment Rate    : {(master['IsPaymentLate']=='Yes').mean()*100:.1f}%")
print(f"  High Risk Customers  : {(customer_metrics['RiskCategory']=='High Risk').sum()}")
print("="*60)
print("\n  Output files saved to: data/processed/")
print("  ✓ o2c_master_dataset.csv")
print("  ✓ customer_risk_scores.csv")
print("  ✓ monthly_revenue_trend.csv")
print("  ✓ kpi_summary.csv")
print("\n  Ready to import into Power BI!")
