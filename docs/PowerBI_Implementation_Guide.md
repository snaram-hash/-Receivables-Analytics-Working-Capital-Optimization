# Power BI Implementation Guide: Receivables Analytics

## 1. Data Modeling (Star Schema)
To build a high-performance Power BI dashboard, configure the following relationships in the Model View:
- **Contractor_Master** (Dimension Table) `1 --> *` **Invoice_Table** (Fact Table) via `contractor_id`
- **Invoice_Table** (Fact Table) `1 --> *` **Payment_Table** (Fact Table) via `invoice_id`
- Create a **Date Table** (Dimension) and link:
  - `Date[Date] 1 --> * Invoice_Table[invoice_date]`
  - `Date[Date] 1 --> * Invoice_Table[due_date]`
  - `Date[Date] 1 --> * Payment_Table[payment_date]`

---

## 2. Core DAX Measures

### Total Outstanding Receivables
```dax
Total Receivables = 
CALCULATE(
    SUM(Invoice_Table[invoice_amount]),
    Invoice_Table[status] = "Open"
)
```

### Overdue Receivables
```dax
Overdue Receivables = 
CALCULATE(
    SUM(Invoice_Table[invoice_amount]),
    Invoice_Table[status] = "Open",
    Invoice_Table[due_date] < TODAY()
)
```

### Collection Rate (Current Month)
```dax
Collection Rate % = 
VAR TotalDueThisMonth = 
    CALCULATE(
        SUM(Invoice_Table[invoice_amount]),
        MONTH(Invoice_Table[due_date]) = MONTH(TODAY()),
        YEAR(Invoice_Table[due_date]) = YEAR(TODAY())
    )
VAR TotalPaidThisMonth = 
    CALCULATE(
        SUM(Payment_Table[amount_paid]),
        MONTH(Payment_Table[payment_date]) = MONTH(TODAY()),
        YEAR(Payment_Table[payment_date]) = YEAR(TODAY())
    )
RETURN DIVIDE(TotalPaidThisMonth, TotalDueThisMonth, 0)
```

### Days Sales Outstanding (DSO) - 12 Month Rolling
```dax
DSO (12M Rolling) = 
VAR TotalAR = [Total Receivables]
VAR CreditSales12M = 
    CALCULATE(
        SUM(Invoice_Table[invoice_amount]),
        DATESINPERIOD('Date'[Date], MAX('Date'[Date]), -12, MONTH)
    )
RETURN DIVIDE(TotalAR, CreditSales12M, 0) * 365
```

### Aging Buckets (Calculated Column on Invoice_Table)
```dax
Aging Bucket = 
VAR DaysLate = DATEDIFF(Invoice_Table[due_date], TODAY(), DAY)
RETURN 
SWITCH(
    TRUE(),
    Invoice_Table[status] = "Paid", "Paid",
    DaysLate <= 0, "Current",
    DaysLate <= 30, "1-30 Days",
    DaysLate <= 60, "31-60 Days",
    DaysLate <= 90, "61-90 Days",
    "90+ Days"
)
```

---

## 3. Executive Dashboard Layout

### Page 1: Executive Summary (The CFO View)
**Goal:** High-level liquidity snapshot.
- **Top KPI Cards:** Total Receivables, Overdue Receivables, DSO, Current Collection Rate %.
- **Line Chart:** Receivables vs. Collections Trend (Last 12 Months).
- **Donut Chart:** Overdue Receivables by Risk Segment (High, Medium, Low).

### Page 2: Receivables & Aging Analysis
**Goal:** Deep dive into invoice aging.
- **Matrix Visual:** Rows: `Contractor Name`, Columns: `Aging Bucket`, Values: `Total Receivables`. Apply red conditional formatting to 60+ days.
- **Stacked Bar Chart:** Outstanding Receivables by Industry (X-axis) and Aging Bucket (Legend).

### Page 3: Contractor Risk Intelligence (Pareto Analysis)
**Goal:** Identify the 20% of clients causing 80% of cash flow problems.
- **Table Visual:** Top 10 Delayed Payers (`Contractor Name`, `Overdue Receivables`, `Average Days Late`).
- **Scatter Plot:** X-Axis: `Credit Limit`, Y-Axis: `Average Days Late`, Size: `Total Receivables`. This highlights large clients who consistently pay late.

### Page 4: Cash Flow Forecasting
**Goal:** Predict short-term liquidity.
- **Waterfall Chart:** Showing starting cash, expected inflows (based on due dates of current open invoices), and historical default rates.
