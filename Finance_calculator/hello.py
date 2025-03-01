from ast import In
from re import X
from personal_calculators import Budget_planner, Car_Loan_emi, Emergency_fund, Retirement_planning, Savings_goal
import streamlit as st
st.set_page_config(page_title="FinSight")

# Importing the pages
landing_page = st.Page(
    page = "landing_page.py",
    title = "Landing Page",
    icon = ":material/home:",
	default = True,
)

Home_Loan_Repayment_Calculator = st.Page(
	page = "personal_calculators/Home_Loan_Repayment_Calculator.py",
	title = "Home Loan Repayments Calculator",

)

Budget_planner = st.Page(
	page = "personal_calculators/Budget_planner.py",
	title = "Budget Planner",
)

SIP_Calculator = st.Page(
	page = "Investment_calculators/SIP_calculator.py",
	title = "SIP Calculator",
	

)

FD_Calculator = st.Page(
	page = "Investment_calculators/FD_calculator.py",
	title = "FD Calculator",
	
)

RD_Calculator = st.Page(
	page = "Investment_calculators/RD_calculator.py",
	title = "RD Calculator",
)

CAGR_Calculator = st.Page(
	page = "Investment_calculators/CAGR_calculator.py",
	title = "CAGR Calculator",
)
Car_Loan_emi = st.Page(
	page = "personal_calculators/Car_Loan_emi.py",
    title = "Car Loan EMI Calculator",
)

Savings_goal = st.Page(
	page = "personal_calculators/Savings_goal.py",
	title = "Savings Goal Calculator",
)

Emergency_fund = st.Page(
	page = "personal_calculators/Emergency_fund.py",
	title = "Emergency Fund Calculator",
)

Income_tax = st.Page(
	page = "personal_calculators/Income_tax.py",
	title = "Income Tax Calculator",
)

Retirement_planning = st.Page(
	page = "personal_calculators/Retirement_planning.py",
	title = "Retirement Planning Calculator",
)

pg = st.navigation(pages=[landing_page,Home_Loan_Repayment_Calculator, SIP_Calculator, FD_Calculator, RD_Calculator, CAGR_Calculator, Car_Loan_emi, Budget_planner, Savings_goal, Emergency_fund, Income_tax, Retirement_planning])

pg = st.navigation(
    {
        "": [landing_page],
		"Investment Calculators": [SIP_Calculator, FD_Calculator, RD_Calculator, CAGR_Calculator],
        "Personal Finance": [Budget_planner,Savings_goal ,Home_Loan_Repayment_Calculator, Car_Loan_emi, Emergency_fund, Income_tax, Retirement_planning],
        
    }
)

st.markdown(
    """
    <style>
    .main .block-container > div:nth-child(1) { /* Target the logo container */
        display: flex;
        justify-content: center; /* Center horizontally */
        align-items: center;     /* Center vertically (if needed) */
    }
    .main .block-container > div:nth-child(1) img { /* Target the logo image */
        max-width: 200px; /* Adjust as needed */
        height: auto;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.logo("assets/logo.png")
st.sidebar.text("Personal Finance & Investment Hub")

pg.run()