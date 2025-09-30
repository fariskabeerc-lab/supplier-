import streamlit as st
import pandas as pd
import plotly.express as px

# --- Title ---
st.title("Supplier Sales & Profit Performance Dashboard")

# --- Load Data ---
file_path = "supplierwise sep sales AUD.Xlsx"  # replace with your file
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

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
    Profit_Margin=('Total Profit', lambda x: (x.sum() / filtered_df['Net Sales (incl. VAT)'].sum()) * 100 if filtered_df['Net Sales (incl. VAT)'].sum() > 0 else 0)
).reset_index().sort_values(by='Total_Sales', ascending=False)

st.subheader("Supplier Summary")
st.dataframe(supplier_summary.style.format({
    "Total_Sales": "{:,.2f}",
    "Total_Profit": "{:,.2f}",
    "Profit_Margin": "{:,.2f}%"
}))

# --- Normal Vertical Bar Graph (Sales + Profit) ---
st.subheader("Suppliers: Sales vs Profit")

fig = px.bar(
    supplier_summary,
    x="Supplier",
    y="Total_Sales",
    text="Total_Sales",
    color="Total_Profit",  # use profit as a factor for coloring
    color_continuous_scale="RdYlGn",  # green = high profit, red = low profit
    title="Suppliers by Sales Value (Colored by Profit)"
)

fig.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside',
    marker_line_width=1.5,
    marker_line_color="black"
)

fig.update_layout(
    xaxis_title="Supplier",
    yaxis_title="Total Sales",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(245,245,245,1)",
    margin=dict(l=50, r=50, t=50, b=120),
    font=dict(size=13)
)

st.plotly_chart(fig, use_container_width=True)

# --- Key Insights ---
st.subheader("Key Supplier Insights")
if not supplier_summary.empty:
    top_supplier = supplier_summary.iloc[0]
    st.markdown(f"- **Top Supplier by Sales:** {top_supplier['Supplier']}")
    st.markdown(f"- **Total Sales:** {top_supplier['Total_Sales']:,.2f}")
    st.markdown(f"- **Total Profit:** {top_supplier['Total_Profit']:,.2f}")
    st.markdown(f"- **Profit Margin (relative to total):** {top_supplier['Profit_Margin']:.2f}%")
