
import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("lulu_sales_data.csv")

st.set_page_config(layout="wide")
st.title("📊 Lulu UAE Sales Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
store_filter = st.sidebar.multiselect("Select Store:", df["Store"].unique(), default=df["Store"].unique())
category_filter = st.sidebar.multiselect("Select Category:", df["Category"].unique(), default=df["Category"].unique())
age_filter = st.sidebar.multiselect("Select Age Group:", df["AgeGroup"].unique(), default=df["AgeGroup"].unique())
gender_filter = st.sidebar.multiselect("Select Gender:", df["Gender"].unique(), default=df["Gender"].unique())
loyalty_filter = st.sidebar.multiselect("Loyalty Member:", df["LoyaltyMember"].unique(), default=df["LoyaltyMember"].unique())

# Apply filters
filtered_df = df[
    (df["Store"].isin(store_filter)) &
    (df["Category"].isin(category_filter)) &
    (df["AgeGroup"].isin(age_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["LoyaltyMember"].isin(loyalty_filter))
]

st.metric("Total Sales", f"AED {filtered_df['SalesAmount'].sum():,.2f}")
st.metric("Avg Sales per Transaction", f"AED {filtered_df['SalesAmount'].mean():,.2f}")
st.metric("Ad Spend (Total)", f"AED {filtered_df['AdvertisementSpend'].sum():,.2f}")

# Show dataset
st.subheader("Filtered Sales Data")
st.dataframe(filtered_df)

# Charts
st.subheader("Sales by Category")
st.bar_chart(filtered_df.groupby("Category")["SalesAmount"].sum())

st.subheader("Sales by Age Group")
st.bar_chart(filtered_df.groupby("AgeGroup")["SalesAmount"].sum())

st.subheader("Sales by Nationality")
st.bar_chart(filtered_df.groupby("Nationality")["SalesAmount"].sum())
