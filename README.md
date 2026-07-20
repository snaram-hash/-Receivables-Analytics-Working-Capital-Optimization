<div align="center">

# Receivables Analytics & Working Capital Optimization
### *Turning delayed payments into predictable cash flow.*

[![SQL](https://img.shields.io/badge/SQL-Advanced_Analytics-blue.svg?style=for-the-badge&logo=sqlite&logoColor=white)](#)
[![Power BI](https://img.shields.io/badge/Power_BI-DAX_%7C_Data_Modeling-yellow.svg?style=for-the-badge&logo=powerbi&logoColor=black)](#)
[![Methodology](https://img.shields.io/badge/Methodology-Enterprise_Consulting-black.svg?style=for-the-badge)](#)

</div>

## 📖 Case Study Context: Apex Industrial Solutions

Apex Industrial Solutions, a leading B2B supplier of heavy machinery and manufacturing equipment, boasts strong on-paper profitability with ₹4.5 Cr in monthly billing. However, the company began experiencing severe liquidity constraints, forcing the Treasury department to repeatedly draw down on high-interest, short-term credit facilities to cover operational expenses and payroll.

An initial audit revealed a stark disconnect between recognized revenue and cash-on-hand. The company was effectively acting as a zero-interest bank for its enterprise clients, with the average **Days Sales Outstanding (DSO) ballooning to 85 days**. The finance team lacked the analytical infrastructure to pinpoint which specific clients were exploiting their payment terms and dynamically forecast short-term cash flow gaps.

**This Analytics Platform was engineered to diagnose, expose, and mathematically resolve these working capital bottlenecks.**

---

## 🎯 Project Overview
Designed as an enterprise-grade finance analytics engagement, this project provides a comprehensive **Receivables Intelligence & Working Capital Optimization System**. By migrating from static, month-end Excel reporting to an active SQL and Power BI ecosystem, the solution allows CFOs and Credit Controllers to transition from reactive debt collection to proactive liquidity management.

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
