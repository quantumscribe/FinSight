import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import altair as alt

st.title("SIP Calculator")

st.write("### Input Data")

monthly_investment = st.slider("Monthly Investment Amount", min_value=0, max_value=100000, value=10000, step=1000)
annual_returns = st.slider("Expected Annual Returns (in %)", min_value=0, max_value=50, value=12, step=1)
investment_period = st.slider("Investment Period (in years)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)



# Convert percentage to decimal
r = annual_returns / 100
n = 12  # Monthly compounding

# Total Amount Invested
amount_invested = monthly_investment * 12 * investment_period

# Correct SIP Future Value Formula
FV = monthly_investment * ((((1 + r / n) ** (n * investment_period)) - 1) / (r / n)) * (1 + r / n)

# Gain
gain = FV - amount_invested

st.write("### 📊 Results")
st.write(f"💰 **Total Amount Invested:** ₹{amount_invested:,.2f}")
st.write(f"📈 **Future Value of Investment:** ₹{FV:,.2f}")
st.write(f"📊 **Total Gain (ROI):** ₹{gain:,.2f}")

# --- Visualization ---
st.write("### 📉 Investment Breakdown")

# Generate Data for Graph (Monthly Compounding)
years = list(range(1, int(investment_period) + 1))
invested_values = [monthly_investment * 12 * y for y in years]  # Total Invested Over Time
investment_growth = [
    monthly_investment * (((1 + r / n) ** (n * y) - 1) / (r / n)) * (1 + r / n)
    for y in years
]  # Future Value at Each Year

# Create DataFrame for Chart
growth_df = pd.DataFrame({
    "Year": years * 2,
    "Value": invested_values + investment_growth,
    "Category": ["Invested Amount"] * len(years) + ["Investment Value"] * len(years),
})

# Create Altair Chart
chart = (
    alt.Chart(growth_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Value:Q", title="Amount (₹)"),
        color="Category",
        tooltip=["Year", "Category", alt.Tooltip("Value:Q", format=",.2f")],  # Hover Card
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)


# --- Table ---
st.write("### Investment Data Table")

table_data = []
for y in years:
    invested = monthly_investment * 12 * y
    future_val = monthly_investment * (((1 + r / n) ** (n * y) - 1) / (r / n)) * (1 + r / n)
    table_data.append({"Year": y, "Invested Amount": invested, "Investment Value": future_val})

df_table = pd.DataFrame(table_data)
st.dataframe(df_table)