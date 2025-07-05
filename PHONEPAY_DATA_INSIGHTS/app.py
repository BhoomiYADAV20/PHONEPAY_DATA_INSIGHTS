import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", layout="wide")

# Header
st.markdown("""
    <h1 style='text-align: center; color: #6C3483;'>📱 PhonePe Pulse Dashboard</h1>
    <p style='text-align: center;'>Explore state-wise, district-wise, and brand-wise digital transaction trends in India</p>
    <hr style='border-top: 2px solid #bbb;'>
""", unsafe_allow_html=True)

# Load datasets
@st.cache_data
def load_data():
    df_txn = pd.read_csv("state_transaction_data.csv")
    df_user = pd.read_csv("state_user_device_data.csv")
    df_map = pd.read_csv("district_transaction_data.csv")
    return df_txn, df_user, df_map

df_txn, df_user, df_map = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
year = st.sidebar.selectbox("Select Year", sorted(df_txn["year"].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(df_txn["quarter"].unique()))
view_type = st.sidebar.radio("View Type", ["Top States", "Districts", "Device Brands", "Transaction Type Share"])

# Filtered data
filtered_txn = df_txn[(df_txn["year"] == year) & (df_txn["quarter"] == quarter)]

# Layout
col1, col2 = st.columns([2, 3])

with col1:
    st.metric("Total Transactions", f"{filtered_txn['count'].sum():,}")
    st.metric("Total Amount (Cr)", f"₹ {filtered_txn['amount'].sum()/1e7:.2f} Cr")

# Views
if view_type == "Top States":
    st.subheader(f"Top 10 States by Transaction Amount - {year} Q{quarter}")
    top_states = filtered_txn.groupby("state")["amount"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_states, x="amount", y="state", orientation="h", color="amount", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

elif view_type == "Districts":
    st.subheader(f"Top 10 Districts by Transaction Amount - {year} Q{quarter}")
    filtered_map = df_map[(df_map["year"] == year) & (df_map["quarter"] == quarter)]
    top_districts = filtered_map.groupby("district")["amount"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_districts, x="amount", y="district", orientation="h", color="amount", color_continuous_scale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

elif view_type == "Device Brands":
    st.subheader(f"Top 10 Device Brands Used - {year} Q{quarter}")
    filtered_user = df_user[(df_user["year"] == year) & (df_user["quarter"] == quarter)]
    brand_totals = filtered_user.groupby("brand")["count"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.pie(brand_totals, names="brand", values="count", title="Device Usage Share", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

elif view_type == "Transaction Type Share":
    st.subheader(f"Transaction Type Breakdown - {year} Q{quarter}")
    txn_type_share = filtered_txn.groupby("type")["amount"].sum().reset_index()
    fig = px.pie(txn_type_share, names="type", values="amount", title="Transaction Type Share", hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; color: gray; font-size: 14px;">
        Made  by <b>Bhoomi</b>
    </div>
""", unsafe_allow_html=True)
