import streamlit as st
import pandas as pd
import plotly.express as px

# --- Title ---
st.title("SAFA oud mehta Supplier Sales Performance Dashboard")

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

# --- Top Suppliers Horizontal Bar Chart ---
st.subheader("Top Suppliers by Net Sales")
fig = px.bar(
    supplier_summary, 
    x='Total_Sales', 
    y='Supplier', 
    text='Total_Sales', 
    orientation='h',  # horizontal bars
    color='Total_Sales',
    color_continuous_scale='Viridis',
    height=500
)

# --- Improve spacing and layout ---
fig.update_traces(
    texttemplate='%{text:,.0f}',  # format numbers with commas
    textposition='outside',       # show values outside bars
    marker_line_width=1.5,       # border around bars
    marker_line_color='black'
)

fig.update_layout(
    yaxis=dict(autorange="reversed"),  # highest at top
    margin=dict(l=150, r=50, t=50, b=50),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(245,245,245,1)',
    font=dict(size=14),
)

st.plotly_chart(fig, use_container_width=True)

# --- Key Insights ---
st.subheader("Key Supplier Insights")
if not supplier_summary.empty:
    top_supplier = supplier_summary.iloc[0]
    st.markdown(f"- **Top Supplier by Sales:** {top_supplier['Supplier']}")
    st.markdown(f"- **Total Sales:** {top_supplier['Total_Sales']:,.2f}")
    st.markdown(f"- **Total Profit:** {top_supplier['Total_Profit']:,.2f}")
    st.markdown(f"- **Number of Distinct Items Supplied:** {top_supplier['Items_Sold']}")

