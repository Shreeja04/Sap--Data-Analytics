# 📊 End-to-End Order-to-Cash (O2C) Analytics System

> **Capstone Project | SAP Business Data Cloud Concepts**

| Field | Details |
|-------|---------|
| **Author** | Shreeja Ghosh |
| **Roll Number** | 2330048 |
| **Project Type** | End-to-End Data Analytics Capstone |
| **Domain** | SAP SD + FI / ERP Analytics |
| **Tech Stack** | Python · Pandas · Power BI · CSV |

---

## 🎯 Project Overview

This project simulates a real-world **Order-to-Cash (O2C)** business process using SAP SD (Sales & Distribution) and FI (Financial Accounting) concepts. It demonstrates how enterprises track the journey of a customer order — from the moment it's placed to the moment payment is received — and extract actionable KPIs using data analytics.

---

## 🔄 The O2C Process Covered

```
Customer Order → Delivery → Invoice → Payment
     ↓               ↓           ↓         ↓
  Sales Order    Logistics    Billing   Collections
  (SAP SD)       (SAP SD)    (SAP FI)   (SAP FI)
```

---

## 📂 Project Structure

```
O2C_Analytics/
│
├── data/
│   ├── raw/                    ← Original simulated datasets
│   │   ├── customers.csv
│   │   ├── sales_orders.csv
│   │   ├── deliveries.csv
│   │   ├── invoices.csv
│   │   └── payments.csv
│   │
│   └── processed/              ← Python output files
│       ├── o2c_master_dataset.csv
│       ├── customer_risk_scores.csv
│       ├── monthly_revenue_trend.csv
│       └── kpi_summary.csv
│
├── scripts/
│   └── process_data.py         ← Main Python processing script
│
├── dashboard_guide/
│   └── PowerBI_Guide.md        ← Step-by-step Power BI instructions
│
├── docs/
│   └── O2C_Project_Report.md   ← Full project documentation
│
└── README.md                   ← This file
```

---

## 📊 Key KPIs Calculated

| KPI | Value |
|-----|-------|
| Total Revenue | ₹1,54,93,500 |
| Total Orders | 40 |
| Unique Customers | 20 |
| Avg O2C Cycle Time | 60.7 days |
| Avg Delivery Delay | 1.7 days |
| Late Delivery Rate | 60% |
| Late Payment Rate | 40% |

---

## 🧠 Advanced Analytics Features

1. **Customer Risk Scoring** — Customers scored as Low / Medium / High Risk based on payment and delivery behavior
2. **Revenue Trend Analysis** — Monthly revenue trend with % growth tracking
3. **Delivery Delay Analysis** — By customer, logistics partner, and order priority

---

## 🛠️ How to Run This Project

### Prerequisites
- Python 3.8 or higher
- pandas library: `pip install pandas numpy`
- Power BI Desktop (free download from Microsoft)

### Steps

**Step 1: Clone this repository**
```bash
git clone https://github.com/YOUR_USERNAME/O2C-Analytics.git
cd O2C-Analytics
```

**Step 2: Install dependencies**
```bash
pip install pandas numpy
```

**Step 3: Run the Python script**
```bash
cd scripts
python process_data.py
```

**Step 4: Open Power BI**
- Import files from `data/processed/`
- Follow instructions in `dashboard_guide/PowerBI_Guide.md`

---

## 🖥️ Dashboard Screenshots

> *(Add your Power BI screenshots here after building the dashboard)*

- [ ] Page 1: Executive Overview
- [ ] Page 2: Delivery & Payment Analysis
- [ ] Page 3: Customer Intelligence

---

## 📋 Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.x | Data processing and KPI calculation |
| Pandas | Data manipulation and merging |
| NumPy | Numerical operations |
| Power BI Desktop | Dashboard creation and visualization |
| CSV | Data storage format |
| Git/GitHub | Version control and submission |

---

## 📈 Business Value

This project demonstrates:
- How to integrate SAP-style transactional data across modules
- How to calculate O2C cycle KPIs used in real enterprise environments
- How to build interactive dashboards for business decision-making
- How to identify high-risk customers and take proactive action

---

## 👤 Author

**Shreeja Ghosh**  
Roll No.: 2330048  
Capstone Project | SAP Business Data Cloud

---

*This project was created for academic purposes to simulate SAP SD+FI analytics using Python and Power BI.*
