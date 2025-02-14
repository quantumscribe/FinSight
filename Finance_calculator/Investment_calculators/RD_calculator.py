import streamlit as st
import pandas as pd

st.title("Recurring Deposit (RD) Calculator")

st.write("### Input Data")

monthly_deposit = st.number_input("Monthly Deposit Amount (₹)", min_value=0, value=10000, step=1000)
annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=7.0, step=0.5)
investment_period = st.number_input("Investment Period (in months)", min_value=0, value=12, step=1)  # RD period is usually in months

# Convert annual interest rate to monthly rate
r = annual_interest_rate / 100 / 12

# Calculate the future value (maturity amount)
FV = monthly_deposit * (((1 + r) ** investment_period - 1) / r) * (1 + r)

# Calculate total amount deposited
total_deposited = monthly_deposit * investment_period

# Calculate total interest earned
interest_earned = FV - total_deposited

st.write("### 📊 Results")
st.write(f"💰 **Total Amount Deposited:** ₹{total_deposited:,.2f}")
st.write(f"📈 **Maturity Amount:** ₹{FV:,.2f}")
st.write(f"💸 **Total Interest Earned:** ₹{interest_earned:,.2f}")

# --- Table (Optional - shows year-wise breakdown) ---
show_table = st.checkbox("Show Year-wise Breakdown")

if show_table:
    table_data = []
    for y in range(1, int(investment_period / 12) + 1): # Loop through years
        start_month = (y - 1) * 12 + 1
        end_month = y * 12
        fv_year = 0  # Initialize future value for the year

        for m in range(start_month, end_month + 1):  # Loop through months of the year
             fv_year += monthly_deposit * (((1 + r) ** (end_month - m + 1) - 1) / r) * (1 + r) if m!=end_month else monthly_deposit*(1+r)

        total_deposited_year = monthly_deposit * 12
        interest_year = fv_year - total_deposited_year if y == 1 else fv_year - table_data[-1]['Future Value'] if table_data else 0
        table_data.append({"Year": y, "Future Value": fv_year, "Interest Earned": interest_year, "Total Deposit": total_deposited_year})

    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table)