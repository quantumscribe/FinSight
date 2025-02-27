import streamlit as st

# Set a wider page layout
# st.set_page_config(layout="wide")

# Title and Subtitle
st.title("Emergency Fund")
st.markdown("<h2 style='text-align: center;'>How much are you planning for an emergency fund?</h2>", unsafe_allow_html=True)

# Input Columns with Placeholders
col1, col2 = st.columns(2)

with col1:
    goal_amount = st.number_input("Emergency Fund Goal (₹)", min_value=0.0, step=1.0, 
                                 placeholder="Enter Goal Amount", key="goal_amount")  # Placeholder added

with col2:
    time_period_years = st.slider("Time Period (Years)", min_value=1, max_value=30, value=5, step=1, key="time_period")
    st.write(f"<div style='text-align: center;'>{time_period_years} Year(s)</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    current_savings = st.number_input("Current Savings (₹)", min_value=0.0, step=1.0, 
                                     placeholder="Enter Current Savings", key="current_savings")  # Placeholder added

with col4:
    monthly_savings = st.number_input("Monthly Savings (₹)", min_value=0.0, step=1.0, 
                                     placeholder="Enter Monthly Savings", key="monthly_savings")  # Placeholder added


# Submit Button
if st.button("SUBMIT"):
    # ... (rest of the calculation and output code remains the same)
    if goal_amount <= 0:
        st.warning("Emergency fund goal must be greater than zero.")
    elif monthly_savings < 0:
        st.warning("Monthly savings cannot be negative.")
    else:
        # Calculations
        time_period_months = time_period_years * 12  # Convert years to months

        if current_savings >= goal_amount:
            st.success("You've already reached your emergency fund goal!")
        elif monthly_savings > 0:
            remaining_amount = goal_amount - current_savings
            if remaining_amount > 0:
                months_to_goal = remaining_amount / monthly_savings
                st.write(f"It will take approximately {months_to_goal:.2f} months to reach your goal.")
            else:
                st.write("You've already reached your goal!")
        else:
            st.write(f"Amount needed: ₹{goal_amount - current_savings:.2f}")
            st.info("Consider a savings plan.")


# Informational expander
with st.expander("Why have an emergency fund?"):
    st.write("An emergency fund is your financial safety net. It helps you cover unexpected expenses like job loss, medical bills, or car repairs without going into debt.")
    st.write("A common recommendation is to save 3-6 months of living expenses, but this can vary based on your personal circumstances.")