# O2C Analytics System — Project Documentation Report

**Project Title:** End-to-End Order-to-Cash (O2C) Analytics System  
**Author:** Shreeja Ghosh  
**Roll Number:** 2330048  
**Subject:** SAP Business Data Cloud Concepts  
**Submission Date:** 2024  

---

## 1. PROBLEM STATEMENT

### Business Context
In large enterprises, the Order-to-Cash (O2C) process spans multiple departments — Sales, Logistics, Finance, and Collections. Data is stored in separate SAP modules (SD for Sales & Distribution, FI for Financial Accounting), making it difficult to get a unified view of performance.

### The Problem
Without a centralized analytics system:
- Management cannot track how long it takes from a customer placing an order to cash being received
- Delivery delays go unnoticed until customers complain
- Late-paying customers continue to receive credit, increasing financial risk
- Revenue trends are invisible, making planning difficult

### Business Questions This Project Answers
1. What is our average Order-to-Cash cycle time?
2. Which customers are causing delivery or payment delays?
3. Which customers are at risk of defaulting on payments?
4. How is our monthly revenue trending?
5. Which product categories and regions are most profitable?

---

## 2. SOLUTION

### Approach
This project builds a complete, end-to-end analytics pipeline that:
1. Simulates realistic transactional data across 5 SAP-style tables
2. Processes and integrates data using Python (Pandas)
3. Calculates key O2C KPIs
4. Presents insights through a multi-page Power BI dashboard

### System Architecture

```
[RAW DATA (CSV)]
   customers.csv
   sales_orders.csv      →  [Python Script]  →  [Processed CSVs]  →  [Power BI Dashboard]
   deliveries.csv            process_data.py      master_dataset
   invoices.csv                                   risk_scores
   payments.csv                                   revenue_trend
                                                  kpi_summary
```

### The O2C Process Simulated

| Stage | SAP Module | Dataset Used | Key Fields |
|-------|-----------|--------------|------------|
| Order Creation | SAP SD | sales_orders.csv | OrderDate, TotalOrderValue |
| Delivery | SAP SD | deliveries.csv | ActualDeliveryDate, DeliveryStatus |
| Invoicing | SAP FI | invoices.csv | InvoiceDate, InvoiceDueDate |
| Payment | SAP FI | payments.csv | PaymentDate, PaymentAmount |

---

## 3. FEATURES

### 3.1 Data Simulation
- 20 real Indian enterprise customers (Tata, Infosys, Reliance, etc.)
- 40 sales orders across Q1-Q2 2024
- Realistic variations in delivery delays and payment behavior
- Multiple product categories (Software, Hardware, Services)

### 3.2 Data Processing (Python)
- Automatic date parsing and validation
- Multi-table join producing a 35-column master dataset
- Zero missing values after cleaning
- Modular, commented, beginner-friendly code

### 3.3 KPI Calculations

| KPI | Formula | Business Use |
|-----|---------|-------------|
| O2C Cycle Time | PaymentDate − OrderDate | Measures process efficiency |
| Delivery Delay | ActualDeliveryDate − PlannedDeliveryDate | Logistics performance |
| Payment Delay | PaymentDate − InvoiceDueDate | Collections efficiency |
| Late Delivery Rate | (Late Deliveries / Total) × 100 | SLA compliance |
| Late Payment Rate | (Late Payments / Total) × 100 | Credit risk indicator |

### 3.4 Advanced Analytics
**Customer Risk Scoring:**
- Assigns each of the 20 customers a risk category (Low/Medium/High)
- Based on: average payment delay, frequency of late payments, delivery issues
- Enables proactive credit management decisions

**Revenue Trend Analysis:**
- Month-over-month revenue growth calculation
- Peak and trough identification
- Supports forecasting and quota setting

### 3.5 Power BI Dashboard
**Page 1 – Executive Overview:**
- 5 KPI cards (Revenue, Orders, Cycle Time, Delivery Rate, Payment Rate)
- Revenue by Customer (Bar Chart)
- Orders by Product Category (Donut)
- Monthly Revenue Trend (Line Chart)

**Page 2 – Operational Performance:**
- Delivery Delay by Customer
- On-Time vs Late Deliveries (Pie)
- Payment Delay Analysis
- Orders by Logistics Partner

**Page 3 – Customer Intelligence:**
- Revenue by Customer Segment (Treemap)
- Risk Distribution (Donut)
- Scatter Plot: Delivery vs Payment Delay
- Top 10 Revenue Customers

---

## 4. TECH STACK

| Component | Technology | Version |
|-----------|-----------|---------|
| Programming Language | Python | 3.8+ |
| Data Manipulation | Pandas | 2.x |
| Numerical Computing | NumPy | 1.x |
| Visualization | Power BI Desktop | Latest |
| Data Format | CSV | — |
| Version Control | Git + GitHub | — |
| Documentation | Markdown | — |

---

## 5. UNIQUE POINTS

1. **India-Specific Dataset:** Uses real Indian enterprises (TCS, Infosys, Reliance) with correct GST formats, Indian regions, and INR currency — making it highly relevant.

2. **SAP Terminology Mapping:** All fields and processes are named using SAP SD/FI terminology (Order → Delivery → Invoice → Payment), demonstrating SAP process knowledge.

3. **End-to-End Pipeline:** Unlike projects that only do visualization, this project covers the full pipeline: data creation → cleaning → merging → KPI calculation → analytics → dashboard.

4. **Customer Risk Intelligence:** The risk scoring system mimics real-world credit risk management used in SAP FSCM (Financial Supply Chain Management).

5. **Beginner-to-Expert Structure:** The code is written with detailed comments that explain both the Python syntax AND the business reason for each step.

---

## 6. RESULTS & INSIGHTS

### KPI Summary

| KPI | Value | Assessment |
|-----|-------|-----------|
| Total Revenue | ₹1,54,93,500 | Strong Q1 performance |
| Avg O2C Cycle Time | 60.7 days | Needs improvement (target: <45 days) |
| Late Delivery Rate | 60% | High — logistics review needed |
| Late Payment Rate | 40% | High — tighten payment terms |
| Medium Risk Customers | 8 | Monitor closely |

### Key Findings

1. **Delivery:** 60% of orders experienced delivery delays. Asian Paints had the worst delay (9 days) due to transit damage. This suggests a need for better packaging standards and logistics partner evaluation.

2. **Payments:** HCL Technologies (62 days), L&T (64 days), and Tata Steel (66 days) consistently pay beyond Net60 terms. These three accounts alone contribute to ₹80+ Lakh in delayed cash.

3. **Revenue Peak:** February 2024 was the highest revenue month (₹53.11 Lakh), driven by SAP implementation projects for Reliance and large hardware orders.

4. **Product Mix:** Services have the highest per-order value (avg ₹4.5 Lakh), while Hardware dominates in volume.

---

## 7. FUTURE SCOPE

1. **Predictive Delay Model:** Train a machine learning model (using scikit-learn) to predict which orders will be delayed based on customer history, order size, and logistics partner.

2. **Real SAP Integration:** Connect to SAP S/4HANA via RFC or OData APIs using the pyrfc or requests library to pull live transaction data.

3. **Automated Reporting:** Schedule the Python script to run daily using Apache Airflow or Windows Task Scheduler, automatically refreshing the Power BI dashboard.

4. **DSO (Days Sales Outstanding) Tracking:** Implement the industry-standard DSO metric and build aging buckets (0-30, 31-60, 61-90, 90+ days) for accounts receivable.

5. **SAP Business Data Cloud Integration:** Migrate this pipeline to SAP Business Data Cloud (BDC) using SAP Datasphere for data integration and SAP Analytics Cloud (SAC) for visualization — the production-grade equivalent of this project.

---

## 8. SCREENSHOTS

*(Add Power BI screenshots here)*

**Screenshot 1:** Executive Overview Dashboard  
`[Insert Page 1 Screenshot]`

**Screenshot 2:** Operational Performance Dashboard  
`[Insert Page 2 Screenshot]`

**Screenshot 3:** Customer Intelligence Dashboard  
`[Insert Page 3 Screenshot]`

**Screenshot 4:** Python Script Execution Output  
`[Insert Terminal Screenshot]`

---

## 9. CONCLUSION

This project successfully demonstrates a complete Order-to-Cash analytics pipeline using SAP process concepts, Python data engineering, and Power BI visualization. The system provides actionable insights for business leaders to improve delivery performance, accelerate cash collection, and manage customer credit risk proactively.

The architecture mirrors real-world enterprise analytics stacks and can be directly evolved into a production system using SAP Business Data Cloud, making it an excellent foundation for a career in SAP analytics and data engineering.

---

*Submitted by: Shreeja Ghosh | Roll No.: 2330048*
