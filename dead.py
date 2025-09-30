import streamlit as st
import pandas as pd
import plotly.express as px

# --- Title ---
st.title("Top Selling Items & Supplier Insights Dashboard")

# --- Load Data ---
file_path = "supplierwise sep sales AUD.Xlsx"  # Replace with your file
df = pd.read_excel(file_path)

# --- Clean Column Names ---
df.columns = df.columns.str.strip()

# --- Sidebar Filters ---
suppliers = ["All"] + sorted(df['Supplier'].dropna().unique().tolist())
categories = ["All"] + sorted(df['Category'].dropna().unique().tolist())

selected_supplier = st.sidebar.selectbox("Select Supplier", suppliers)
selected_category = st.sidebar.selectbox("Select Category", categories)

# --- Apply Filters ---
filtered_df = df.copy()
if selected_supplier != "All":
    filtered_df = filtered_df[filtered_df['Supplier'] == selected_supplier]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

# --- Top Selling Items by Sales Value ---
top_items = filtered_df.groupby(['Item Code', 'Items'])['Net Sales (incl. VAT)'].sum().reset_index()
top_items = top_items.sort_values(by='Net Sales (incl. VAT)', ascending=False).head(10)

st.subheader("Top 10 Selling Items")
st.dataframe(top_items.style.format({"Net Sales (incl. VAT)": "{:,.2f}"}))

# --- Supplier Contribution to Sales ---
supplier_sales = filtered_df.groupby('Supplier')['Net Sales (incl. VAT)'].sum().reset_index()
supplier_sales = supplier_sales.sort_values(by='Net Sales (incl. VAT)', ascending=False)

st.subheader("Supplier Contribution to Sales")
fig1 = px.bar(supplier_sales, x='Supplier', y='Net Sales (incl. VAT)',
              text='Net Sales (incl. VAT)', color='Net Sales (incl. VAT)',
              color_continuous_scale='Viridis')
st.plotly_chart(fig1, use_container_width=True)

# --- Key Insights ---
total_sales = filtered_df['Net Sales (incl. VAT)'].sum()
total_profit = filtered_df['Total Profit'].sum()
total_gross_sales = filtered_df['Gross Sales'].sum()
total_discount = filtered_df['Discount'].sum()
total_excise_value = filtered_df['Excise_Value'].sum()

st.subheader("Key Insights")
st.markdown(f"- **Total Net Sales:** {total_sales:,.2f}")
st.markdown(f"- **Total Profit:** {total_profit:,.2f}")
st.markdown(f"- **Total Gross Sales:** {total_gross_sales:,.2f}")
st.markdown(f"- **Total Discount:** {total_discount:,.2f}")
st.markdown(f"- **Total Excise Value:** {total_excise_value:,.2f}")

# --- Top Items Bar Chart ---
st.subheader("Top Items by Net Sales")
fig2 = px.bar(top_items, x='Items', y='Net Sales (incl. VAT)',
              text='Net Sales (incl. VAT)', color='Net Sales (incl. VAT)',
              color_continuous_scale='Cividis')
st.plotly_chart(fig2, use_container_width=True)
