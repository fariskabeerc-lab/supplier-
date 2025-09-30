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

# --- Add GP% ---
supplier_summary['GP%'] = (supplier_summary['Total_Profit'] / supplier_summary['Total_Sales']) * 100

st.subheader("Supplier Summary")
st.dataframe(supplier_summary.style.format({
    "Total_Sales": "{:,.2f}",
    "Total_Profit": "{:,.2f}",
    "Total_Gross_Sales": "{:,.2f}",
    "Total_Discount": "{:,.2f}",
    "GP%": "{:,.2f}%"
}))

# --- Top 20 Suppliers Horizontal Bar Chart ---
st.subheader("Top 20 Suppliers by Net Sales (Horizontal)")
top20_suppliers = supplier_summary.nlargest(20, 'Total_Sales')

fig = px.bar(
    top20_suppliers.sort_values('Total_Sales', ascending=True),  # sort for horizontal display
    y='Supplier', x='Total_Sales',
    text='Total_Sales', color='Total_Sales',
    color_continuous_scale='Viridis',
    orientation='h'
)
fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
fig.update_layout(
    yaxis=dict(title="Supplier", automargin=True),
    xaxis=dict(title="Net Sales"),
    bargap=0.4
)
st.plotly_chart(fig, use_container_width=True)

# --- Key Insights ---
st.subheader("Key Supplier Insights")
top_supplier = supplier_summary.iloc[0]
st.markdown(f"- **Top Supplier by Sales:** {top_supplier['Supplier']}")
st.markdown(f"- **Total Sales:** {top_supplier['Total_Sales']:,.2f}")
st.markdown(f"- **Total Profit:** {top_supplier['Total_Profit']:,.2f}")
st.markdown(f"- **Gross Profit % (GP%):** {top_supplier['GP%']:.2f}%")
st.markdown(f"- **Number of Distinct Items Supplied:** {top_supplier['Items_Sold']}")
