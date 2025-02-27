import streamlit as st
import pandas as pd

# st.set_page_config(layout="wide")

# Title and Subtitle
st.title("Retirement Planner")
st.markdown("<h2 style='text-align: center;'>Plan your retirement with ease</h2>", unsafe_allow_html=True)

# Input Column (All inputs in one column)
with st.container():
    current_age = st.slider("Current Age (15-60 Years)", min_value=15, max_value=60, value=30, step=1)
    retirement_age = st.slider("Desired Retirement Age (Upto 70 Years)", min_value=current_age, max_value=70, value=60, step=1)
    life_expectancy = st.slider("Life Expectancy (Upto 100 Years)", min_value=retirement_age, max_value=100, value=80, step=1)
    monthly_income_retirement = st.number_input("Monthly Income Required in Retirement Years (₹)", min_value=0, step=1, value=10000)
    inflation_rate = st.slider("Expected Inflation Rate (%) (Normal Inflation Rate In India Is 3%-15%)", min_value=3, max_value=15, value=6, step=1) / 100
    return_on_investment_preretirement = st.slider("Expected Return On Investment (Pre-retirement) (%)", min_value=0.0, max_value=20.0, value=15.0, step=0.5) / 100
    return_on_investment_postretirement = st.slider("Expected Return On Investment (Post-retirement) (%)", min_value=0.0, max_value=20.0, value=6.0, step=0.5) / 100
    existing_savings = st.number_input("Do You Have Any Existing Saving Or Investment For Retirement? (₹)", min_value=0, step=1, value=10000)

# Calculation Function
def calculate_retirement_corpus(current_age, retirement_age, life_expectancy, monthly_income_retirement, inflation_rate, return_on_investment_preretirement, return_on_investment_postretirement, existing_savings):
    if current_age >= retirement_age or retirement_age >= life_expectancy:
        return None, None, None, None  # Handle invalid input

    years_to_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age

    future_monthly_expenses = monthly_income_retirement * (1 + inflation_rate)**years_to_retirement

    corpus = existing_savings * (1 + return_on_investment_preretirement/12)**(years_to_retirement*12)

    discount_rate = (1 + return_on_investment_postretirement/12)
    required_corpus = 0
    for year in range(years_in_retirement):
        for month in range(12):
            required_corpus += (future_monthly_expenses) / (discount_rate**(year*12 + month))

    additional_corpus_needed = max(0, required_corpus - corpus)

    if years_to_retirement > 0:
        monthly_savings = additional_corpus_needed * (return_on_investment_preretirement/12) / (((1 + return_on_investment_preretirement/12)**(years_to_retirement*12) - 1) )
    else:
        monthly_savings = 0

    return additional_corpus_needed, years_in_retirement, future_monthly_expenses, monthly_savings


# Calculate Button
if st.button("Calculate"):
    if current_age < 15 or retirement_age > 70 or life_expectancy > 100 or current_age >= retirement_age or retirement_age >= life_expectancy or monthly_income_retirement < 0 or inflation_rate < 0 or return_on_investment_preretirement < 0 or return_on_investment_postretirement < 0 or existing_savings < 0:
        st.warning("Please enter valid input values within the specified ranges.")
    else:
        additional_corpus_needed, years_in_retirement, future_monthly_expenses, monthly_savings = calculate_retirement_corpus(current_age, retirement_age, life_expectancy, monthly_income_retirement, inflation_rate, return_on_investment_preretirement, return_on_investment_postretirement, existing_savings)

        if additional_corpus_needed is not None:
            st.markdown(f"<div style='font-size: 20px; font-weight: bold;'>Annual Income Required<br>Immediately After Retirement</div><div style='font-size: 20px;'>₹ {future_monthly_expenses * 12:,.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 20px; font-weight: bold;'>Additional Retirement Fund Which<br>Needs To Be Accumulated Is</div><div style='font-size: 20px;'>₹ {additional_corpus_needed:,.2f}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 20px; font-weight: bold;'>Monthly Savings Required To<br>Accumulate The Fund Is</div><div style='font-size: 20px;'>₹ {monthly_savings:,.2f}</div>", unsafe_allow_html=True)
            st.write(f"Years in Retirement: {years_in_retirement}")
        else:
            st.warning("Invalid input. Please check your age, retirement age, and life expectancy.")


# Disclaimer
st.markdown("<small>Disclaimer: This calculator is for informational purposes only and does not constitute financial advice. Consult with a financial advisor for personalized planning.</small>", unsafe_allow_html=True)