import streamlit as st
import pandas as pd
import plotly.express as px

# --- Title ---
st.title("Supplier Sales Performance Dashboard")

# --- Load Data ---
file_path = "supplierwise sep sales AUD.Xlsx"  # replace with your Excel file
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()  # clean column names

# --- Sidebar Filters ---
suppliers = ["All"] + sorted(df['Supplier'].dropna().unique())
categories = ["All"] + sorted(df['Category'].dropna().unique())

selected_supplier = st.sidebar.selectbox("Select Supplier", suppliers)
selected_category = st.sidebar.selectbox("Select Category", categories)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_supplier != "All":
    filtered_df = filtered_df[filtered_df['Supplier'] == selected_supplier]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# --- Supplier-wise Aggregation ---
supplier_summary = filtered_df.groupby('Supplier').agg(
    Total_Sales=('Net Sales (incl. VAT)', 'sum'),
    Total_Profit=('Total Profit', 'sum'),
    Total_Gross_Sales=('Gross Sales', 'sum'),
    Total_Discount=('Discount', 'sum'),
    Items_Sold=('Items', 'nunique')  # number of distinct items
).reset_index().sort_values(by='Total_Sales', ascending=False)

st.subheader("Supplier Summary")
st.dataframe(supplier_summary.style.format({
    "Total_Sales": "{:,.2f}",
    "Total_Profit": "{:,.2f}",
    "Total_Gross_Sales": "{:,.2f}",
    "Total_Discount": "{:,.2f}"
}))

# --- Top Suppliers Bar Chart ---
st.subheader("Top Suppliers by Net Sales")
fig = px.bar(
    supplier_summary, 
    x='Supplier', y='Total_Sales', 
    text='Total_Sales', color='Total_Sales',
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig, use_container_width=True)

# --- Key Insights ---
st.subheader("Key Supplier Insights")
top_supplier = supplier_summary.iloc[0]
st.markdown(f"- **Top Supplier by Sales:** {top_supplier['Supplier']}")
st.markdown(f"- **Total Sales:** {top_supplier['Total_Sales']:,.2f}")
st.markdown(f"- **Total Profit:** {top_supplier['Total_Profit']:,.2f}")
st.markdown(f"- **Number of Distinct Items Supplied:** {top_supplier['Items_Sold']}")
