# E-Commerce Sales Analytics & Automated SQL Reporting

An end-to-end **retail analytics and automated reporting system** built on MySQL, Python, SQL, Power BI, and a local LLM.

The project combines an interactive Power BI dashboard with an automated SQL reporting workflow that can detect failed queries, inspect the database schema, determine the root cause, and use an AI agent to explain the failure and suggest a fix.

## 🚀 Project Overview

This project started as an e-commerce analytics dashboard and was extended into a practical **analytics automation and data reliability workflow**.

It answers recurring business questions such as:

- What were the total sales for a reporting date?
- How many orders were placed?
- What was the average order value?
- Which product categories generated the most revenue?
- Which states generated the most orders?
- How did delivery performance vary?
- Which payment methods were most commonly used?

The automated workflow then handles these reports without requiring manual SQL execution.

---

## 🏗️ Architecture

```text
                    E-Commerce Dataset
                           |
                           v
                    MySQL Database
                           |
             +-------------+-------------+
             |                           |
             v                           v
        SQL Analysis                Power BI
             |                           |
             v                           v
      Business KPIs              Interactive Dashboard
             |
             v
      Automated Python Runner
             |
             v
       Data Validation
             |
        +----+----+
        |         |
     Success    Failure
        |         |
        v         v
   JSON Report   Schema Inspection
                    |
                    v

📊 Power BI Dashboard
1. Executive Sales Overview

Key metrics:

Total Sales: 13.59M
Total Orders: ~99K
Average Order Value: 136.68
Average Delivery Days: 12.18
Monthly sales trend
             Deterministic Analysis
                    |
                    v
             AI Investigation
                    |
                    v
        Root Cause + Evidence + Fix
