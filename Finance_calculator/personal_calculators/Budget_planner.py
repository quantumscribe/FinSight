import streamlit as st
import pandas as pd
import plotly.express as px

# st.set_page_config(page_title="Budget Planner", page_icon=":money_with_wings:")

st.title("Budget Planner")

if "budget_data" not in st.session_state:
    st.session_state.budget_data = pd.DataFrame(columns=["Category", "Description", "Amount", "Type"])

if "income_types" not in st.session_state:
    st.session_state.income_types = [
        "Salary (Net)",
        "Business Income",
        "Freelance Income",
        "Rental Income",
        "Dividends",
        "Interest Income",
        "Side Hustle Income",
        "Pension/Annuity",
        "Child Support",
        "Reimbursements",
        "One-Time Bonus",
        "Other Income",
    ]
if "expense_types" not in st.session_state:
    st.session_state.expense_types = [
        "Rent",
        "Utilities",
        "Food",
        "Transportation",
        "Entertainment",
        "Shopping",
        "Healthcare",
        "Education",
        "Travel",
        "Home Improvement",
        "Dining Out",
        "Groceries",
        "Personal Care",
        "Clothing",
        "Gifts",
        "Donations",
        "Subscriptions",
        "Childcare",
        "Pet Expenses",
        "Debt Payments",
        "Insurance",
        "Taxes",
        "Other Expense",
    ]

st.subheader("Add Income/Expense")

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Category", ["Income", "Expense"], key="category")

with col2:
    if category == "Income":
        type_options = st.session_state.income_types
    else:
        type_options = st.session_state.expense_types

    item_type = st.selectbox("Type", type_options, key="type")

    if item_type == "Other Income" or item_type == "Other Expense":
        other_type = st.text_input("Other Type", key="other_type", placeholder="Specify other type")
        final_type = other_type if other_type else item_type
        if other_type:
            if category == "Income":
                if other_type not in st.session_state.income_types:
                    st.session_state.income_types.append(other_type)
            else:
                if other_type not in st.session_state.expense_types:
                    st.session_state.expense_types.append(other_type)
            st.rerun()
    else:
        final_type = item_type

with st.form("budget_form"):
    description = st.text_area("Description (Optional)", key="description", placeholder="e.g., Rent for April, Salary from Company X")
    amount = st.number_input("Amount", min_value=0.0, step=1.0, key="amount", placeholder="Enter amount")
    submitted = st.form_submit_button("Add Item")

if submitted:
    if amount:
        new_item = pd.DataFrame({"Category": [category], "Amount": [amount], "Type": [final_type], "Description": [description]})
        st.session_state.budget_data = pd.concat([st.session_state.budget_data, new_item], ignore_index=True)
    else:
        st.warning("Please enter the Amount.")

st.subheader("Budget Summary")

if not st.session_state.budget_data.empty:
    summary_df = st.session_state.budget_data.copy()

    if hasattr(st, "experimental_data_editor"):
        edited_df = st.experimental_data_editor(summary_df, key="budget_editor")
        indices_to_delete = [i for i, row in edited_df.iterrows() if row["Delete"]]
        if indices_to_delete:
            st.session_state.budget_data = st.session_state.budget_data.drop(indices_to_delete).reset_index(drop=True)
            st.rerun()
    else:
        st.dataframe(summary_df, hide_index=True)
        selected_indices = st.multiselect("Select rows to delete", range(len(summary_df)))
        if st.button("Delete Selected Rows"):
            st.session_state.budget_data = st.session_state.budget_data.drop(selected_indices).reset_index(drop=True)
            st.rerun()

    summary_grouped = st.session_state.budget_data.groupby(["Category", "Type"])["Amount"].sum().reset_index()
    income = st.session_state.budget_data[st.session_state.budget_data["Category"] == "Income"]["Amount"].sum()
    expenses = st.session_state.budget_data[st.session_state.budget_data["Category"] == "Expense"]["Amount"].sum()
    net_balance = income - expenses

    st.write(f"**Total Income:** ₹{income:.2f}")
    st.write(f"**Total Expenses:** ₹{expenses:.2f}")
    st.write(f"**Net Balance:** ₹{net_balance:.2f}")

    fig = px.pie(summary_grouped, 
                 values='Amount', 
                 names='Type', 
                 color='Category', 
                 title='Expense/Income Breakdown',
                 color_discrete_map={"Income": "#2ecc71", "Expense": "#e74c3c"}, # Modern color palette
                 hole=0.3,  # Donut chart for a cleaner look
                 hover_data=['Amount'], # Show amount on hover
                 labels={'Amount': 'Amount (₹)'}) # Label the amount

    fig.update_layout(
        title_font=dict(size=20, color="#34495e", family="Arial, sans-serif"),  # Modern title font
        font=dict(family="Arial, sans-serif", size=14, color="#34495e"),  # Modern font
        plot_bgcolor="#f5f5f5",  # Light background color
        paper_bgcolor="#0e1117",  # Light background color for the chart area
        hoverlabel=dict(bgcolor="#ffffff", bordercolor="#bdc3c7", font=dict(color="#34495e")),  # Style hover information
    )
    fig.update_traces(textposition='inside', textinfo='percent+label') # Show both percent and label inside the chart

    st.plotly_chart(fig)

    csv = st.session_state.budget_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='budget_data.csv',
        mime='text/csv',
    )

else:
    st.write("No budget items added yet.")