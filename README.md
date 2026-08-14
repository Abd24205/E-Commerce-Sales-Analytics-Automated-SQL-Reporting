# E-Commerce Sales & Analytics Automation System

An end-to-end **E-Commerce Analytics and Automated Reporting System** that combines MySQL, SQL, Power BI, Python automation, and a local AI agent to transform raw e-commerce data into business insights and automatically investigate reporting failures.

The project goes beyond a static analytics dashboard by implementing a repeatable reporting workflow that can:

- Analyze e-commerce sales and customer data using SQL
- Generate recurring business reports automatically
- Validate generated metrics
- Detect SQL/reporting failures
- Inspect database schema during failures
- Perform deterministic root-cause analysis
- Use a local LLM to explain failures and suggest fixes
- Visualize business performance through Power BI

---

## 📌 Project Overview

Traditional portfolio analytics projects usually stop after creating SQL queries and a dashboard.

This project extends that workflow into a small-scale **analytics operations system**.

The system combines:

**Data → SQL → Automated Reporting → Validation → Failure Detection → AI Investigation → Business Intelligence**

The project is designed to demonstrate how analytics workflows can be made **repeatable, automated, and resilient to failures**.

---

# 🏗️ Architecture

```text
                    ┌─────────────────────────┐
                    │   Raw E-Commerce Data   │
                    │       Olist Dataset     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      MySQL Database      │
                    │                         │
                    │ customers               │
                    │ orders                  │
                    │ order_items             │
                    │ payments                │
                    │ products                │
                    │ reviews                 │
                    │ sellers                 │
                    │ ecommerce_dashboard     │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
              ▼                                     ▼
    ┌─────────────────────┐              ┌─────────────────────┐
    │      SQL Analysis   │              │      Power BI       │
    │                     │              │                     │
    │ Business Queries    │              │ Data Model          │
    │ KPI Calculations    │              │ DAX Measures        │
    │ Aggregations        │              │ Interactive Reports │
    └──────────┬──────────┘              └─────────────────────┘
               │
               ▼
    ┌─────────────────────────┐
    │ Python Reporting Engine │
    │                         │
    │ Execute SQL             │
    │ Validate Results        │
    │ Generate JSON Reports   │
    │ Log Failures            │
    └────────────┬────────────┘
                 │
          ┌──────┴──────┐
          │             │
       SUCCESS        FAILURE
          │             │
          ▼             ▼
    ┌────────────┐  ┌─────────────────────┐
    │ Daily JSON │  │ Schema Inspection   │
    │ Report     │  │ + Deterministic     │
    └────────────┘  │ Root Cause Analysis │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Local AI Agent      │
                    │                     │
                    │ Llama 3.2 3B        │
                    │ via Ollama           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ AI Investigation    │
                    │ Report              │
                    │                     │
                    │ Root Cause          │
                    │ Evidence            │
                    │ Suggested Fix       │
                    │ Severity            │
                    └─────────────────────┘

```
## 🎯 Project Objectives

The project was built to solve two related analytics problems:

# 1. Business Intelligence

Provide an interactive view of:

Sales performance
Order volume
Product categories
Customer geography
Delivery performance
Payment behavior
Monthly trends

# 2. Automated Analytics Operations

Create a reporting workflow capable of:

Running recurring SQL reports
Generating machine-readable reports
Validating report outputs
Handling SQL failures
Inspecting database schemas
Identifying root causes
Using AI to explain failures

## 🗄️ Database Structure

The project uses MySQL as the analytical database.

# Main Tables

```text
customers
orders
order_items
payments
products
reviews
sellers
```

ecommerce_dashboard

The main analytical table combines important order, product, payment, seller, and review attributes.

Key fields include:
```text
order_id
customer_id
customer_unique_id
customer_state
order_status
order_purchase_timestamp
order_month
delivery_days
estimated_delivery_days
delivery_delay_days
order_item_id
product_id
seller_id
price
freight_value
product_category
payment_type
payment_installments
payment_value
review_score
```

## 🔄 Analytics Workflow

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
MySQL Database
     ↓
SQL Analysis
     ↓
Power BI Data Model
     ↓
DAX Measures
     ↓
Interactive Dashboard
```

# The automated reporting workflow extends this process:

```text
Scheduled Job
     ↓
Execute SQL Query
     ↓
Validate Results
     ↓
       ┌───────────────┐
       │               │
    SUCCESS         FAILURE
       │               │
       ▼               ▼
Generate JSON     Log Error
Report                 ↓
                  Inspect Schema
                       ↓
               Deterministic Analysis
                       ↓
                   AI Agent
                       ↓
                Investigation Report
```

## 🤖 Automated SQL Reporting

The project includes a Python-based reporting engine that executes SQL queries for a supplied reporting date.

Example:
```text
python -m automation.runner 2018-08-29
```
Example output:
```text
Running Daily Sales Report for 2018-08-29...

Report generated successfully.
Total Sales: 4262.66
Total Orders: 11
Average Order Value: 387.51
```

The generated report is saved as:
```text
The generated report is saved as:
```
Example:
```text
{
    "report_date": "2018-08-29",
    "report_type": "daily_sales",
    "status": "success",
    "metrics": {
        "report_date": "2018-08-29",
        "total_sales": "4262.66",
        "total_orders": 11,
        "average_order_value": "387.51"
    }
}
```

## 📊 Daily Sales SQL
The reporting engine currently calculates:

Total Sales
Total Orders
Average Order Value

Conceptually:
```text
SELECT
    DATE(order_purchase_timestamp) AS report_date,

    ROUND(SUM(payment_value), 2) AS total_sales,

    COUNT(DISTINCT order_id) AS total_orders,

    ROUND(
        SUM(payment_value) /
        COUNT(DISTINCT order_id),
        2
    ) AS average_order_value

FROM ecommerce_dashboard

WHERE DATE(order_purchase_timestamp) = %s

GROUP BY DATE(order_purchase_timestamp);
```
The reporting date is supplied dynamically by the Python automation layer.

## ✅ Report Validation

Generated reports are validated before being saved.

The validation layer checks whether the returned metrics satisfy expected conditions.

Examples include:

Sales value exists
Order count exists
Average order value exists
Metrics contain valid values
Query returned a usable result

This prevents invalid reports from silently being generated.

## 🚨 Failure Handling

The system includes a controlled failure workflow to simulate real-world SQL/reporting problems.

Example:
```text
python -m automation.runner 2018-08-29 --test-failure
```

The test intentionally references a non-existent column:
```text
payment_value_invalid
```
The database returns:
```text
1054 (42S22):
Unknown column 'payment_value_invalid'
in 'field list'
```
The system catches the failure and creates a failure log.

## 🔍 Deterministic Failure Investigation

Before using AI, the system performs deterministic analysis.

The investigation process checks:

SQL error message
Query file
Database table
Available columns
Invalid column references
Whether the referenced column exists

For example:
```text
Error Type:
UNKNOWN_COLUMN

Invalid Column:
payment_value_invalid

Column Exists:
False

Root Cause:
The SQL query references the column
'payment_value_invalid', but that column
does not exist in the ecommerce_dashboard table.

Severity:
HIGH
```
This is important because the AI is not expected to blindly guess the cause.

The system first establishes verified technical facts.

## 🧠 AI Failure Investigation

After deterministic analysis, the system sends the verified context to a local AI model.

The project uses:
```text
Ollama
    ↓
Llama 3.2 3B
```

The AI receives information such as:

SQL error
Query
Query file
Database table
Available columns
Deterministic analysis

The AI then produces a human-readable explanation.

Example:
```text
ROOT CAUSE:

The SQL query references a non-existent column
'payment_value_invalid' in the
'ecommerce_dashboard' table.

EVIDENCE:

The error message indicates that the column
does not exist.

SUGGESTED FIX:

Modify the SQL query to reference an existing
column, such as 'payment_value'.

SEVERITY:

HIGH
```

## 🛡️ Deterministic + AI Architecture

The AI layer is intentionally placed after deterministic validation.
```text
SQL Failure
     ↓
Error Detection
     ↓
Schema Inspection
     ↓
Verified Root Cause
     ↓
AI Explanation
     ↓
Suggested Fix
```
This prevents the LLM from being the only source of truth.

The deterministic layer provides verified evidence, while the LLM provides a more readable explanation and debugging guidance.

## ⏰ Automated Execution

The project includes a Windows batch script:
```text
automation/run_daily_report.bat
```
It can automatically determine the latest available reporting date and execute the reporting workflow.

Example:
```text
==========================================
Automated Daily Sales Reporting
==========================================

Running report for latest available data...

Report Date: 2018-08-29

Running Daily Sales Report for 2018-08-29...

Report generated successfully.

Total Sales: 4262.66
Total Orders: 11
Average Order Value: 387.51

==========================================
Automation completed
==========================================
```
The workflow can be connected to Windows Task Scheduler for recurring execution.

## 📈 Power BI Dashboard

The Power BI dashboard provides an interactive business-facing layer on top of the analytical data.

# 1. Executive Sales Overview

Key metrics:

Total Sales: 13.59M
Total Orders: ~99K
Average Order Value: 136.68
Average Delivery Days: 12.18
Monthly sales trend

# 2. Product & Category Analysis

Analysis includes:

Sales by product category
Orders by product category
Average order value by category
Category performance comparison

# 3. Delivery & Customer Analysis

Analysis includes:

On-time vs late deliveries
Average delivery time by state
Orders by state
Geographic performance

# 4. Payment & Order Trends

Analysis includes:

Revenue by payment method
Orders by payment method
Monthly order trends
Payment behavior

## 📐 Key DAX Measures

# Total Sales
```text
Total Sales =
SUM('ecommerce_dashboard'[payment_value])
```
# Total Orders
```text
Total Orders =
DISTINCTCOUNT('orders'[order_id])
```
# Average Order Value
```text
Average Order Value =
DIVIDE(
    [Total Sales],
    [Total Orders]
)
```

# Average Delivery Days
```text
Average Delivery Days =
AVERAGE('orders'[delivery_days])
```

## 📊 Key Business Findings

The analysis identified several important business patterns:

Total sales reached approximately 13.59M across approximately 99K orders.
bed_bath_table is one of the strongest categories by sales and order volume.
computers shows a high average order value among displayed categories.
Approximately 92.14% of orders were delivered on time.
São Paulo (SP) is the dominant market by order volume and sales.
Credit card is the dominant payment method by both order volume and payment value.
Sales and order activity increased substantially through 2017, with November 2017 representing a major peak.

## 💡 Business Recommendations

Based on the analysis:

# 1. Focus on High-Performing Categories

Maintain strong inventory availability and promotional activity for high-performing categories.

# 2. Investigate High-AOV Products

High average-order-value categories can be evaluated for:

Premium product opportunities
Cross-selling
Upselling

# 3. Improve Logistics

Investigate states and regions with higher delivery times to identify potential logistics bottlenecks.

# 4. Prepare for Seasonal Demand

Historical sales peaks can be used to improve:

Inventory planning
Staffing
Fulfillment capacity
Promotional planning

# 5. Optimize Payment Experience

Continue optimizing the dominant credit-card checkout experience while encouraging alternative payment methods.

## 📁 Project Structure

```text
Retail-Sales-E-Commerce-Analytics-Dashboard/
│
├── automation/
│   ├── ai_agent/
│   │   ├── error_analyzer.py
│   │   ├── investigator.py
│   │   ├── llm_investigator.py
│   │   └── test_*.py
│   │
│   ├── queries/
│   │   ├── daily_sales.sql
│   │   └── daily_sales_test_failure.sql
│   │
│   ├── reports/
│   │   └── daily_sales_reports.json
│   │
│   ├── logs/
│   │   └── ai_investigation.txt
│   │
│   ├── database.py
│   ├── error_handler.py
│   ├── investigation.py
│   ├── runner.py
│   ├── schema_inspector.py
│   ├── validation.py
│   └── run_daily_report.bat
│
├── dashboard/
│   └── ecommerce_dashboard.pbix
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── images/
│   ├── page1-executive-overview.png
│   ├── page2-product-category.png
│   ├── page3-delivery-customer.png
│   └── page4-payment-orders.png
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── sql/
│   └── analysis.sql
│
├── .env.example
├── .gitignore
└── README.md
```
## 🛠️ Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| **Python**       | Automation and reporting        |
| **MySQL**        | Analytical database             |
| **SQL**          | Business analysis and reporting |
| **Power BI**     | Interactive visualization       |
| **DAX**          | KPI calculations                |
| **Power Query**  | Data transformation             |
| **Ollama**       | Local LLM execution             |
| **Llama 3.2 3B** | AI failure investigation        |
| **Git/GitHub**   | Version control                 |

## 🧪 Testing

The project includes controlled failure tests for the investigation workflow.

Successful Report
```text
python -m automation.runner 2018-08-29
```

Expected:

Report generated successfully.

Failure Test:
```text
python -m automation.runner 2018-08-29 --test-failure
```
Expected:

REPORT FAILED:
Error: Unknown column 'payment_value_invalid'

The failure then passes through:

Error Handler
      ↓
Schema Inspector
      ↓
Deterministic Investigator
      ↓
Local LLM Investigator

## 🔐 Configuration
