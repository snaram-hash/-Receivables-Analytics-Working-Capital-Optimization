<div align="center">

# Receivables Analytics & Working Capital Optimization
### *Turning delayed payments into predictable cash flow.*

[![SQL](https://img.shields.io/badge/SQL-Advanced_Analytics-blue.svg?style=for-the-badge&logo=sqlite&logoColor=white)](#)
[![Power BI](https://img.shields.io/badge/Power_BI-DAX_%7C_Data_Modeling-yellow.svg?style=for-the-badge&logo=powerbi&logoColor=black)](#)
[![Deloitte Framework](https://img.shields.io/badge/Methodology-Deloitte_Consulting-black.svg?style=for-the-badge)](#)

</div>

## Monday Morning at 9:00 AM
The CFO walks into the weekly Treasury meeting. The payroll for 275 security guards is due on Friday. 

He asks:
> *"Why are we dipping into our high-interest credit line again? We billed ₹4.5 Cr last month!"*

The answer lies buried in the ERP system. 
Sales says the clients are "good for it." Operations says the invoices were sent on time. 
But the reality is that the company is effectively acting as a free bank for its contractors. Average Days Sales Outstanding (DSO) has slipped to 85 days, and nobody knows exactly which clients are abusing the payment terms.

**This Analytics Platform exists to expose those bottlenecks and optimize working capital.**

---

## 🎯 Project Overview
A Deloitte-style consulting engagement designed for a mid-sized Security Services Company facing severe working capital constraints. Despite high on-paper profitability, recurring payment delays of 60–90 days from enterprise contractor accounts are creating massive cash flow gaps.

This project delivers an end-to-end **Receivables Intelligence System** using SQL and Power BI to transition the finance department from reactive collections to proactive, data-driven liquidity management.

---

## 📈 Business Impact (Before vs. After)

| Problem Area | Before Analytics | After Analytics |
| :--- | :--- | :--- |
| **Collections Strategy** | Alphabetical / Random calling | Targeted, risk-weighted prioritization |
| **Visibility** | Month-end static Excel reports | Real-time Power BI Aging Dashboards |
| **Working Capital** | Heavy reliance on short-term debt | Optimized liquidity, predictable inflows |
| **Client Risk** | Unknown concentration | Identified Top 20% causing 80% delays |
| **DSO Tracking** | Estimated intuitively | Mathematically calculated 12M Rolling |

---

## 🏛️ Technical Implementation

### 1. The Data Foundation (Python & SQL)
A robust data generation engine (`infrastructure/data_generator.py`) simulates a 3NF relational database tracking 34 enterprise contractors over 24 months. 
- Injects realistic enterprise delays (e.g., *Payments Modernization Gateway* failing to pay on time).
- Enforces the Pareto Principle (80/20 rule) where a subset of clients causes the majority of the aging balances.

### 2. The Core Analytics Engine (SQL)
Advanced SQL queries (`sql/analytics_queries.sql`) power the underlying logic:
- **Invoice Aging Analysis:** Standard 0-30, 31-60, 61-90, 90+ bucketing.
- **DSO Calculation:** Days Sales Outstanding modeling.
- **Contractor Risk Scoring:** Identifying late-payment patterns.
- **Pareto Analysis:** Ranking clients by cumulative overdue percentages.

### 3. The Executive Dashboard (Power BI)
A fully documented DAX and Data Modeling implementation (`docs/PowerBI_Implementation_Guide.md`) designed to be plugged directly into Power BI Desktop.
- Features dynamic measures for `Collection Rate %`, `DSO (12M Rolling)`, and `Overdue Receivables`.

---

## 📚 Consulting Artifacts
Explore the full engagement documentation in the `/docs` directory:
- [Business Case & Problem Statement](docs/Business_Case.md): The financial impetus for the project.
- [Power BI Implementation Guide](docs/PowerBI_Implementation_Guide.md): The DAX dictionary and layout specs.
- [Consulting Recommendations](docs/Consulting_Recommendations.md): Actionable strategies to reduce DSO by 30 days.

---
<div align="center">
  <i>Engineered for Enterprise Financial Intelligence</i>
</div>
