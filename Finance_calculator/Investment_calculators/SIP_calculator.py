import streamlit as st
import pandas as pd
import math
import altair as alt

st.title("SIP Calculator")

st.write("### Input Data")

monthly_investment = st.slider("Monthly Investment Amount (P)", min_value=0.0, max_value=100000.0, value=10000.0, step=1000.0)
annual_returns = st.slider("Expected Annual Returns (in %) (Annual i)", min_value=0.0, max_value=50.0, value=12.0, step=1.0)
investment_period = st.slider("Investment Period (in years)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)

monthly_rate = (annual_returns / 100) / 12
total_payments = int(investment_period * 12)
future_value = monthly_investment * (((1 + monthly_rate)**total_payments - 1) / monthly_rate) * (1 + monthly_rate)
total_invested = monthly_investment * total_payments
total_gain = future_value - total_invested

def format_indian_currency(number):
    s = str(round(number, 2))
    if '.' in s:
        integer_part, decimal_part = s.split('.')
    else:
        integer_part, decimal_part = s, '00'
    integer_part = integer_part[::-1]
    formatted_integer = ','.join(integer_part[i:i+3] for i in range(0, len(integer_part), 3))
    formatted_integer = formatted_integer[::-1]
    if len(formatted_integer) > 3:
        formatted_integer = formatted_integer[0:3] + ',' + formatted_integer[3:].replace(',', '', formatted_integer[3:].count(',') -1)

    return f"{formatted_integer}.{decimal_part}"

st.write("### 📊 Results")
st.write(f"💰 **Total Amount Invested** ₹{format_indian_currency(total_invested)}")
st.write(f"📈 **Future Value of Investment :** ₹{format_indian_currency(future_value)}")
st.write(f"📊 **Total Gain :** ₹{format_indian_currency(total_gain)}")

st.write("### 📉 Investment Breakdown")

years = list(range(1, int(investment_period) + 1))
invested_values = [monthly_investment * 12 * y for y in years]

investment_growth = []
for y in years:
    months_y = y * 12
    future_val = monthly_investment * (((1 + monthly_rate)**months_y - 1) / monthly_rate) * (1 + monthly_rate)
    investment_growth.append(future_val)

growth_df = pd.DataFrame({
    "Year": years * 2,
    "Value": invested_values + investment_growth,
    "Category": ["Invested Amount"] * len(years) + ["Investment Value"] * len(years),
})

chart = (
    alt.Chart(growth_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Value:Q", title="Amount (₹)"),
        color="Category",
        tooltip=["Year", "Category", alt.Tooltip("Value:Q", format=",.2f")],
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.write("### Investment Data Table")

table_data = []
for y in years:
    invested = monthly_investment * 12 * y
    months_y = y * 12
    future_val = monthly_investment * (((1 + monthly_rate)**months_y - 1) / monthly_rate) * (1 + monthly_rate)
    table_data.append({"Year": y, "Invested Amount": format_indian_currency(invested), "Investment Value": format_indian_currency(future_val)})

df_table = pd.DataFrame(table_data)

st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .dataframe {
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="center">', unsafe_allow_html=True)
st.dataframe(df_table)
st.markdown('</div>', unsafe_allow_html=True)

st.write("### Learn about SIP")

with st.expander("What is SIP?"):
    st.write(
        """
        SIP stands for Systematic Investment Plan. It's a method of investing in mutual funds where you invest a fixed amount of money at regular intervals (usually monthly). 
        It allows you to invest small amounts regularly, making it easier to build wealth over time.
        """
    )

with st.expander("How does the SIP formula work?"):
    st.write(
        """
        The SIP formula is: 
        **M = P × ({[1 + i]^n - 1} / i) × (1 + i)**
        Where:
        * M = Amount received upon maturity
        * P = Amount invested at regular intervals
        * n = Number of payments made
        * i = Periodic rate of interest
        This formula calculates the future value of your SIP investments, considering compound interest.
        """
    )

with st.expander("Understanding Interest Rates in SIP"):
    st.write(
        """
        The interest rate in SIP is the expected rate of return on your investment. It's usually expressed as an annual percentage.
        The monthly rate (i) is calculated by dividing the annual rate by 12.
        Remember, the interest rate can fluctuate based on market conditions, affecting your returns.
        """
    )

with st.expander("Impact of Investment Period"):
    st.write(
        """
        The longer your investment period (n), the more time your money has to grow through compounding.
        Even small monthly investments can accumulate into a substantial amount over a long period.
        Longer investment periods also help mitigate the impact of market volatility.
        """
    )

with st.expander("Why Invest in SIP?"):
    st.write(
        """
        * **Rupee-Cost Averaging:** SIPs help you buy more units when the market is low and fewer units when the market is high, averaging out your purchase cost.
        * **Power of Compounding:** Your returns earn returns, leading to exponential growth over time.
        * **Disciplined Investing:** SIPs encourage regular investing, fostering financial discipline.
        * **Affordability:** You can start with small amounts, making it accessible to most investors.
        """
    )