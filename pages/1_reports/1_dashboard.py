import streamlit as st
import plotly.express as px
import sys
import os

# Ensure the root project path is available for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from models.exposures._exp_jaffle_shop_dashboard import exp_jaffle_shop_dashboard
from models.marts.jaffle_shop._dim_customers import dim_customers
from models.marts.payments._fct_payments import fct_payments

st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("📊 Executive Dashboard")
st.markdown("This generic dashboard serves as a boilerplate starting point to visualize your core data platform structures.")

# Fetch data from models
df_dashboard = exp_jaffle_shop_dashboard()
df_customers = dim_customers()
df_payments = fct_payments()

# Global metrics
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_revenue = df_dashboard['total_revenue'].sum()
total_orders = df_dashboard['total_orders'].sum()
total_customers = len(df_customers)
active_payments = len(df_payments)

col1.metric("Total Revenue", f"${total_revenue:,.2f}", "10% YoY")
col2.metric("Total Orders", f"{total_orders}", "2% YoY")
col3.metric("Total Customers", f"{total_customers}")
col4.metric("Total Transactions", f"{active_payments}")

st.divider()

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Order Status Distribution")
    fig_status = px.pie(df_dashboard, values='total_orders', names='status', hole=0.4, title="Orders by Status")
    st.plotly_chart(fig_status, use_container_width=True)

with col_right:
    st.subheader("Revenue by Order Status")
    fig_revenue = px.bar(df_dashboard, x='status', y='total_revenue', color='status', title="Revenue Contribution")
    st.plotly_chart(fig_revenue, use_container_width=True)

st.divider()

# Tables
st.subheader("Data Previews")
tab1, tab2, tab3 = st.tabs(["Dashboard Summary", "Customer Dimension", "Transaction Facts"])

with tab1:
    st.dataframe(df_dashboard, use_container_width=True)

with tab2:
    st.dataframe(df_customers, use_container_width=True)

with tab3:
    st.dataframe(df_payments, use_container_width=True)
