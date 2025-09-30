import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Supplier Sales & Profit Performance Dashboard")

# --- Load Excel File directly ---
file_path = "supplierwise sep sales AUD.Xlsx"  # make sure this file is in the same folder
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# --- Aggregate by Supplier ---
supplier_summary = df.groupby('Supplier').agg(
    Total_Sales=('Net Sales (incl. VAT)', 'sum'),
    Total_Profit=('Total Profit', 'sum')
).reset_index().sort_values(by='Total_Sales', ascending=False)

# --- Simple Bar Chart ---
st.subheader("Suppliers by Sales & Profit")
fig = go.Figure()

# Sales Bars
fig.add_trace(go.Bar(
    x=supplier_summary["Supplier"],
    y=supplier_summary["Total_Sales"],
    name="Total Sales",
    marker_color="skyblue"
))

# Profit Bars
fig.add_trace(go.Bar(
    x=supplier_summary["Supplier"],
    y=supplier_summary["Total_Profit"],
    name="Total Profit",
    marker_color="lightgreen"
))

fig.update_layout(
    barmode='group',  # show side-by-side bars
    xaxis_title="Supplier",
    yaxis_title="Value",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=12),
    margin=dict(l=40, r=40, t=40, b=120)
)

st.plotly_chart(fig, use_container_width=True)

# --- Table View ---
st.subheader("Supplier Summary Table")
st.dataframe(supplier_summary.style.format({
    "Total_Sales": "{:,.2f}",
    "Total_Profit": "{:,.2f}"
}))
