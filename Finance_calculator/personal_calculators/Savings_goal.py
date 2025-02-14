import streamlit as st

st.title("Savings Goal Calculator")

# Input sliders (with reasonable ranges and steps)
goal_amount = st.slider("Savings Goal Amount", min_value=0.0, max_value=1000000.0, value=50000.0, step=1000.0)
current_savings = st.slider("Current Savings", min_value=0.0, max_value=goal_amount, value=10000.0, step=500.0)
monthly_contribution = st.slider("Monthly Contribution", min_value=0.0, max_value=20000.0, value=5000.0, step=500.0)
time_period_months = st.slider("Time Period (Months)", min_value=1, max_value=60, value=12, step=1)

# Calculate button
if st.button("Calculate"):  # The button is now *inside* the conditional block
    if goal_amount <= current_savings:
        st.warning("Your current savings already meet or exceed your goal!")
    elif monthly_contribution == 0 and (goal_amount > current_savings):
        st.warning("You need to contribute monthly to reach your goal.")
    elif time_period_months == 0:
        st.warning("Time period must be greater than 0")
    else:
        amount_needed = goal_amount - current_savings
        if monthly_contribution > 0:
            months_to_reach_goal = (amount_needed / monthly_contribution)
            if months_to_reach_goal <= time_period_months:
                st.success(f"You will reach your goal in approximately {int(months_to_reach_goal)} months!")
            else:
                st.warning(f"With current contributions, it will take {int(months_to_reach_goal)} months to reach the goal. Consider increasing your monthly contribution or extending the time period.")

        else:
            st.warning("You need to contribute monthly to reach your goal.")

        # Additional calculations
        total_saved = current_savings + (monthly_contribution * time_period_months)
        st.write(f"Total savings after {time_period_months} months: ₹{total_saved:.2f}")

        if total_saved < goal_amount and time_period_months > 0:
            additional_monthly = (goal_amount - total_saved) / time_period_months
            st.write(f"You need to contribute an additional ₹{additional_monthly:.2f} monthly to reach your goal by the deadline.")

# The rest of the code (output display) remains *outside* the conditional block
# ... (no changes needed here)