import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px

# Configuration
st.set_page_config(page_title="Receivables Analytics", layout="wide", page_icon="💸")
db_path = os.path.join(os.path.dirname(__file__), "receivables_analytics.db")

def get_connection():
    return sqlite3.connect(db_path)

# --- Fetch Data ---
@st.cache_data
def load_kpis():
    conn = get_connection()
    # Total Outstanding
    total_ar = pd.read_sql_query("SELECT SUM(invoice_amount) as total FROM Invoice_Table WHERE status = 'Open'", conn).iloc[0]['total']
    # Overdue
    overdue_ar = pd.read_sql_query("SELECT SUM(invoice_amount) as total FROM Invoice_Table WHERE status = 'Open' AND due_date < date('now')", conn).iloc[0]['total']
    # DSO Proxy (Total AR / 12M Sales * 365)
    sales = pd.read_sql_query("SELECT SUM(invoice_amount) as total FROM Invoice_Table WHERE invoice_date >= date('now', '-12 months')", conn).iloc[0]['total']
    dso = (total_ar / sales) * 365 if sales else 0
    conn.close()
    return total_ar, overdue_ar, dso

@st.cache_data
def load_aging():
    conn = get_connection()
    query = '''
        SELECT 
            c.contractor_name,
            c.industry,
            i.invoice_amount,
            CAST(julianday('now') - julianday(i.due_date) AS INTEGER) AS days_past_due
        FROM Invoice_Table i
        JOIN Contractor_Master c ON i.contractor_id = c.contractor_id
        WHERE i.status = 'Open'
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Bucketize
    def get_bucket(days):
        if days <= 0: return 'Current'
        elif days <= 30: return '1-30 Days'
        elif days <= 60: return '31-60 Days'
        elif days <= 90: return '61-90 Days'
        else: return '90+ Days'
        
    df['aging_bucket'] = df['days_past_due'].apply(get_bucket)
    return df

@st.cache_data
def load_risk():
    conn = get_connection()
    query = '''
        SELECT 
            c.contractor_name,
            c.credit_limit,
            SUM(i.invoice_amount) AS overdue_balance,
            AVG(CAST(julianday('now') - julianday(i.due_date) AS INTEGER)) as avg_days_late
        FROM Invoice_Table i
        JOIN Contractor_Master c ON i.contractor_id = c.contractor_id
        WHERE i.status = 'Open' AND i.due_date < date('now')
        GROUP BY c.contractor_id, c.contractor_name, c.credit_limit
        ORDER BY overdue_balance DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- UI ---
st.title("Receivables Analytics & Working Capital Optimization")
st.markdown("Turning delayed payments into predictable cash flow.")
st.divider()

# KPIs
st.header("Executive Summary (CFO View)")
total_ar, overdue_ar, dso = load_kpis()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Outstanding AR", f"₹{total_ar/1000000:.2f} Cr")
col2.metric("Overdue Receivables", f"₹{overdue_ar/1000000:.2f} Cr", delta="High Risk", delta_color="inverse")
col3.metric("12M Rolling DSO", f"{dso:.1f} Days", delta="+15 Days target", delta_color="inverse")
col4.metric("AR at Risk (>60 Days)", f"{((overdue_ar/total_ar)*100):.1f}%")

st.divider()

# Aging Analysis
st.header("Receivables & Aging Analysis")
aging_df = load_aging()

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Outstanding Receivables by Aging Bucket")
    aging_summary = aging_df.groupby('aging_bucket')['invoice_amount'].sum().reset_index()
    # Sort buckets logically
    bucket_order = ['Current', '1-30 Days', '31-60 Days', '61-90 Days', '90+ Days']
    aging_summary['aging_bucket'] = pd.Categorical(aging_summary['aging_bucket'], categories=bucket_order, ordered=True)
    aging_summary = aging_summary.sort_values('aging_bucket')
    
    fig = px.bar(aging_summary, x='aging_bucket', y='invoice_amount', color='aging_bucket', 
                 color_discrete_sequence=['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b'])
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Overdue Exposure by Industry")
    ind_summary = aging_df[aging_df['days_past_due'] > 0].groupby('industry')['invoice_amount'].sum().reset_index()
    fig2 = px.pie(ind_summary, values='invoice_amount', names='industry', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Pareto Analysis
st.header("Contractor Risk Intelligence (80/20 Analysis)")
st.markdown("Identify the top clients disproportionately contributing to cash flow gaps.")

risk_df = load_risk()
risk_df['cumulative_overdue'] = risk_df['overdue_balance'].cumsum()
risk_df['cumulative_percent'] = (risk_df['cumulative_overdue'] / risk_df['overdue_balance'].sum()) * 100

st.dataframe(
    risk_df[['contractor_name', 'overdue_balance', 'avg_days_late', 'cumulative_percent']]
    .style.background_gradient(subset=['overdue_balance'], cmap='Reds')
    .format({'overdue_balance': '₹{:,.0f}', 'avg_days_late': '{:.1f} days', 'cumulative_percent': '{:.1f}%'}),
    use_container_width=True
)

if not risk_df.empty:
    worst_offender = risk_df.iloc[0]
    st.error(f"🚨 **Critical Action Required:** Suspend credit limit for **{worst_offender['contractor_name']}**. They currently owe ₹{worst_offender['overdue_balance']:,.0f} and are averaging {worst_offender['avg_days_late']:.1f} days late.")
