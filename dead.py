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

# --- Top Suppliers Horizontal Bar Chart ---
st.subheader("Top Suppliers by Net Sales (Horizontal)")
fig = px.bar(
    supplier_summary,
    y='Supplier', x='Total_Sales',
    text='Total_Sales', color='Total_Sales',
    color_continuous_scale='Viridis',
    orientation='h'  # horizontal
)
fig.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
fig.update_layout(yaxis=dict(title="Supplier", automargin=True),
                  xaxis=dict(title="Net Sales"),
                  bargap=0.4)  # space between bars
st.plotly_chart(fig, use_container_width=True)

# --- High Sales but Low Profit Chart ---
st.subheader("Suppliers with High Sales but Low Profit")
# Define threshold: high sales above median, profit below median
sales_threshold = supplier_summary['Total_Sales'].median()
profit_threshold = supplier_summary['Total_Profit'].median()

high_sales_low_profit = supplier_summary[
    (supplier_summary['Total_Sales'] > sales_threshold) &
    (supplier_summary['Total_Profit'] < profit_threshold)
]

if not high_sales_low_profit.empty:
    fig2 = px.bar(
        high_sales_low_profit,
        y='Supplier', x='Total_Sales',
        text='Total_Profit',
        color='Total_Profit',
        orientation='h',
        color_continuous_scale='Reds'
    )
    fig2.update_traces(texttemplate='Profit: %{text:,.2f}', textposition='outside')
    fig2.update_layout(yaxis=dict(title="Supplier", automargin=True),
                       xaxis=dict(title="Net Sales"),
                       bargap=0.4)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No suppliers found with high sales but low profit.")

# --- Key Insights ---
st.subheader("Key Supplier Insights")
top_supplier = supplier_summary.iloc[0]
st.markdown(f"- **Top Supplier by Sales:** {top_supplier['Supplier']}")
st.markdown(f"- **Total Sales:** {top_supplier['Total_Sales']:,.2f}")
st.markdown(f"- **Total Profit:** {top_supplier['Total_Profit']:,.2f}")
st.markdown(f"- **Number of Distinct Items Supplied:** {top_supplier['Items_Sold']}")

