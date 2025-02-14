import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu


def calculate_tax(income, age_group, financial_year):
    # Define tax slabs based on the financial year and age group
    if financial_year == "2024-2025":
        if age_group == "0-60":
            slabs = [
                (400000, 0.00),
                (800000, 0.05),
                (1200000, 0.10),
                (1600000, 0.15),
                (2000000, 0.20),
                (2400000, 0.25),
                (float('inf'), 0.30)
            ]
        elif age_group == "60-80":
            slabs = [
                (500000, 0.00),
                (1000000, 0.05),
                (1500000, 0.10),
                (2000000, 0.15),
                (2500000, 0.20),
                (3000000, 0.25),
                (float('inf'), 0.30)
            ]
        else:  # age_group == "80 & above"
            slabs = [
                (600000, 0.00),
                (1200000, 0.05),
                (1800000, 0.10),
                (2400000, 0.15),
                (3000000, 0.20),
                (3600000, 0.25),
                (float('inf'), 0.30)
            ]
    else:
        # Default slabs if financial year is not 2024-2025
        slabs = [
            (400000, 0.00),
            (800000, 0.05),
            (1200000, 0.10),
            (1600000, 0.15),
            (2000000, 0.20),
            (2400000, 0.25),
            (float('inf'), 0.30)
        ]

    tax = 0
    previous_slab = 0

    for slab, rate in slabs:
        if income > previous_slab:
            taxable_amount = min(income, slab) - previous_slab
            tax += taxable_amount * rate
            previous_slab = slab
        else:
            break

    return tax

st.title("Income Tax Calculator")

# Financial Year Selection
financial_year = st.selectbox(
    "Select the Financial Year:",
    ("2024-2025", "2023-2024")
)

# Age Group Selection
age_group = st.selectbox(
    "Select your Age Group:",
    ("0-60", "60-80", "80 & above")
)

# Income Input
income = st.number_input("Enter your annual income (in ₹):", min_value=0, step=1000)

if st.button("Calculate Tax"):
    tax = calculate_tax(income, age_group, financial_year)
    st.success(f"Your calculated tax for FY {financial_year} is ₹{tax:,.2f}")
