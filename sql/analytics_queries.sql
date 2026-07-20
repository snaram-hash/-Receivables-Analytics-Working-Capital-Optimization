-- Receivables Analytics & Working Capital Optimization
-- Core Analytics Queries

-- 1. Invoice Aging Analysis (0-30, 31-60, 61-90, 90+ days)
-- Groups outstanding invoices into standard accounting aging buckets based on how far past due they are.
WITH AgingBase AS (
    SELECT 
        c.contractor_id,
        c.contractor_name,
        i.invoice_id,
        i.invoice_amount,
        CAST(julianday('now') - julianday(i.due_date) AS INTEGER) AS days_past_due
    FROM Invoice_Table i
    JOIN Contractor_Master c ON i.contractor_id = c.contractor_id
    WHERE i.status = 'Open'
)
SELECT 
    contractor_name,
    SUM(CASE WHEN days_past_due <= 0 THEN invoice_amount ELSE 0 END) AS current_not_due,
    SUM(CASE WHEN days_past_due > 0 AND days_past_due <= 30 THEN invoice_amount ELSE 0 END) AS aging_1_30_days,
    SUM(CASE WHEN days_past_due > 30 AND days_past_due <= 60 THEN invoice_amount ELSE 0 END) AS aging_31_60_days,
    SUM(CASE WHEN days_past_due > 60 AND days_past_due <= 90 THEN invoice_amount ELSE 0 END) AS aging_61_90_days,
    SUM(CASE WHEN days_past_due > 90 THEN invoice_amount ELSE 0 END) AS aging_90_plus_days,
    SUM(invoice_amount) AS total_outstanding
FROM AgingBase
GROUP BY contractor_id, contractor_name
ORDER BY total_outstanding DESC;

-- 2. Days Sales Outstanding (DSO) Calculation (Last 12 Months)
-- DSO = (Average Accounts Receivable / Total Credit Sales) * Number of Days
WITH MonthlySales AS (
    SELECT 
        strftime('%Y-%m', invoice_date) AS month,
        SUM(invoice_amount) as total_sales
    FROM Invoice_Table
    WHERE invoice_date >= date('now', '-12 months')
    GROUP BY strftime('%Y-%m', invoice_date)
),
ReceivablesSnapshot AS (
    SELECT 
        SUM(invoice_amount) AS total_ar
    FROM Invoice_Table
    WHERE status = 'Open'
)
SELECT 
    (SELECT total_ar FROM ReceivablesSnapshot) AS total_accounts_receivable,
    SUM(total_sales) AS annual_credit_sales,
    ((SELECT total_ar FROM ReceivablesSnapshot) / SUM(total_sales)) * 365 AS days_sales_outstanding
FROM MonthlySales;

-- 3. Pareto Analysis (80/20 Rule) - Top 20% of Contractors Causing 80% of Delays
-- Identifies the high-risk contractors that disproportionately impact working capital.
WITH ContractorAr AS (
    SELECT 
        c.contractor_id,
        c.contractor_name,
        SUM(i.invoice_amount) AS overdue_balance
    FROM Invoice_Table i
    JOIN Contractor_Master c ON i.contractor_id = c.contractor_id
    WHERE i.status = 'Open' AND i.due_date < date('now')
    GROUP BY c.contractor_id, c.contractor_name
),
TotalAr AS (
    SELECT SUM(overdue_balance) AS total_overdue FROM ContractorAr
),
RankedAr AS (
    SELECT 
        contractor_name,
        overdue_balance,
        SUM(overdue_balance) OVER (ORDER BY overdue_balance DESC) AS cumulative_overdue,
        (SELECT total_overdue FROM TotalAr) AS total_system_overdue
    FROM ContractorAr
)
SELECT 
    contractor_name,
    overdue_balance,
    (cumulative_overdue / total_system_overdue) * 100 AS cumulative_percentage
FROM RankedAr
WHERE (cumulative_overdue / total_system_overdue) <= 0.85 -- Capturing roughly the top 80% impact
ORDER BY overdue_balance DESC;

-- 4. Collection Effectiveness Index (CEI)
-- Measures the percentage of receivables collected within a given time period compared to what was available.
WITH BeginningAR AS (
    SELECT SUM(invoice_amount) AS beg_ar 
    FROM Invoice_Table 
    WHERE invoice_date < date('now', '-30 days') AND (status = 'Open' OR (status = 'Paid' AND invoice_id IN (SELECT invoice_id FROM Payment_Table WHERE payment_date >= date('now', '-30 days'))))
),
MonthlyCreditSales AS (
    SELECT SUM(invoice_amount) AS sales 
    FROM Invoice_Table 
    WHERE invoice_date >= date('now', '-30 days')
),
EndingAR AS (
    SELECT SUM(invoice_amount) AS end_ar 
    FROM Invoice_Table 
    WHERE status = 'Open'
)
SELECT 
    (SELECT beg_ar FROM BeginningAR) AS beginning_ar,
    (SELECT sales FROM MonthlyCreditSales) AS credit_sales,
    (SELECT end_ar FROM EndingAR) AS ending_ar,
    -- CEI Formula: (Beg AR + Sales - End AR) / (Beg AR + Sales - End Current AR) * 100
    -- Simplified for demo to a basic Collection Ratio if strict CEI is unavailable due to current AR bounds.
    ((SELECT beg_ar FROM BeginningAR) + (SELECT sales FROM MonthlyCreditSales) - (SELECT end_ar FROM EndingAR)) / 
    ((SELECT beg_ar FROM BeginningAR) + (SELECT sales FROM MonthlyCreditSales)) * 100 AS collection_effectiveness_index;

-- 5. Contractor Payment Behavior Pattern (Average Delay Days)
SELECT 
    c.contractor_name,
    c.risk_segment,
    COUNT(i.invoice_id) AS total_invoices,
    AVG(CAST(julianday(p.payment_date) - julianday(i.due_date) AS INTEGER)) AS avg_days_late
FROM Invoice_Table i
JOIN Payment_Table p ON i.invoice_id = p.invoice_id
JOIN Contractor_Master c ON i.contractor_id = c.contractor_id
GROUP BY c.contractor_name, c.risk_segment
ORDER BY avg_days_late DESC;
