import streamlit as st
import pandas as pd

st.title("Fixed Deposit (FD) Calculator")

st.write("### Input Data")

principal_amount = st.number_input("Principal Amount (₹)", min_value=0, value=10000, step=1000)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=7.0, step=0.5)
investment_period = st.number_input("Investment Period (in years)", min_value=0, value=1, step=1)
compounding_frequency = st.selectbox("Compounding Frequency", ["Annual", "Semi-Annual", "Quarterly", "Monthly", "Daily"])

# Convert interest rate to decimal
r = interest_rate / 100

# Calculate the number of compounding periods per year
if compounding_frequency == "Annual":
    n = 1
elif compounding_frequency == "Semi-Annual":
    n = 2
elif compounding_frequency == "Quarterly":
    n = 4
elif compounding_frequency == "Monthly":
    n = 12
elif compounding_frequency == "Daily":
    n = 365

# Calculate the future value (maturity amount)
FV = principal_amount * (1 + r / n) ** (n * investment_period)

# Calculate the total interest earned
interest_earned = FV - principal_amount

st.write("### 📊 Results")
st.write(f"💰 **Principal Amount:** ₹{principal_amount:,.2f}")
st.write(f"📈 **Maturity Amount:** ₹{FV:,.2f}")
st.write(f"💸 **Total Interest Earned:** ₹{interest_earned:,.2f}")


# --- Table (Optional - shows year-wise breakdown) ---
show_table = st.checkbox("Show Year-wise Breakdown")

if show_table:
    table_data = []
    for y in range(1, int(investment_period) + 1):
        fv_year = principal_amount * (1 + r / n) ** (n * y)
        interest_year = fv_year - principal_amount if y == 1 else fv_year - table_data[-1]['Future Value'] if table_data else 0
        table_data.append({"Year": y, "Future Value": fv_year, "Interest Earned": interest_year})
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table)