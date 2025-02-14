import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Title of the app
st.title("Car Loan EMI Calculator")

# Input fields
st.header("Loan Details")
loan_amount = st.number_input("Loan Amount (₹):", min_value=0.0, value=500000.0)
interest_rate = st.number_input("Annual Interest Rate (%):", min_value=0.0, value=9.5)
loan_tenure = st.number_input("Loan Tenure (Years):", min_value=1, max_value=30, value=5)

# Convert inputs
monthly_interest_rate = (interest_rate / 100) / 12
loan_tenure_months = loan_tenure * 12

# EMI calculation formula
def calculate_emi(principal, rate, tenure):
    if rate == 0:
        return principal / tenure
    return (principal * rate * (1 + rate) ** tenure) / ((1 + rate) ** tenure - 1)

# Calculate EMI
emi = calculate_emi(loan_amount, monthly_interest_rate, loan_tenure_months)

# Display results
st.header("Results")
st.write(f"**Monthly EMI:** ₹{emi:,.2f}")

# Total payment and interest
total_payment = emi * loan_tenure_months
total_interest = total_payment - loan_amount

st.write(f"**Total Payment:** ₹{total_payment:,.2f}")
st.write(f"**Total Interest Payable:** ₹{total_interest:,.2f}")

# Calculate amortization schedule (always compute this)
balance = loan_amount
amortization_data = []
for month in range(1, loan_tenure_months + 1):
    interest = balance * monthly_interest_rate
    principal = emi - interest
    balance -= principal
    amortization_data.append((month, emi, principal, interest, balance))

# Create DataFrame for amortization schedule
amortization_df = pd.DataFrame(
    amortization_data,
    columns=["Month", "EMI", "Principal", "Interest", "Remaining Balance"]
)

# Show amortization table only if checkbox is checked
st.header("Amortization Schedule")
if st.checkbox("Show Amortization Schedule"):
    st.table(amortization_df.style.format({
        "EMI": "₹{:.2f}",
        "Principal": "₹{:.2f}",
        "Interest": "₹{:.2f}",
        "Remaining Balance": "₹{:.2f}"
    }))

# Visualizations (now uses the pre-computed amortization_df)
st.header("Interactive Visualizations")

# Visualization 1: Principal vs Interest Over Time
st.subheader("Principal vs Interest Over Time")
fig1 = px.line(amortization_df, x="Month", y=["Principal", "Interest"], 
               title="Principal vs Interest Over Time",
               labels={"value": "Amount (₹)", "variable": "Component"})
st.plotly_chart(fig1)

# Visualization 2: Remaining Balance Over Time
st.subheader("Remaining Loan Balance Over Time")
fig2 = px.line(amortization_df, x="Month", y="Remaining Balance", 
               title="Remaining Loan Balance Over Time",
               labels={"Remaining Balance": "Balance (₹)"})
st.plotly_chart(fig2)

# Visualization 3: Pie Chart of Total Payment Breakdown
st.subheader("Total Payment Breakdown")
breakdown_df = pd.DataFrame({
    "Component": ["Principal", "Interest"],
    "Amount": [loan_amount, total_interest]
})
fig3 = px.pie(breakdown_df, values="Amount", names="Component", 
              title="Total Payment Breakdown",
              color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig3)