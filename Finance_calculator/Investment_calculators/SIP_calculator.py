from operator import index
import streamlit as st
import pandas as pd
import math
import altair as alt
from st_aggrid import AgGrid
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

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
    """
    Format a number according to the Indian numbering system (lakhs and crores).
    Example: 1234567.89 becomes 12,34,567.89
    """
    # Round to 2 decimal places and convert to string
    s = str(round(number, 2))
    
    # Split the number into integer and decimal parts
    if '.' in s:
        integer_part, decimal_part = s.split('.')
    else:
        integer_part, decimal_part = s, '00'
    
    # Ensure decimal part has exactly 2 digits
    decimal_part = decimal_part.ljust(2, '0')[:2]
    
    # Format the integer part according to Indian numbering system
    # First, reverse the string to work from right to left
    reversed_int = integer_part[::-1]
    
    # Take the first 3 digits
    groups = [reversed_int[:3][::-1]]
    
    # Then group by 2 digits for the rest
    for i in range(3, len(reversed_int), 2):
        if i + 2 <= len(reversed_int):
            groups.append(reversed_int[i:i+2][::-1])
        else:
            groups.append(reversed_int[i:][::-1])
    
    # Reverse the groups list and join with commas
    formatted_integer = ",".join(groups[::-1])
    
    return f"{formatted_integer}.{decimal_part}"

def get_abbreviated_amount(number):
    """
    Returns an abbreviated form of large numbers in Indian format
    Examples: 
    - 123000 -> "1.23 lakh"
    - 12300000 -> "1.23 crore"
    """
    if number < 1000:
        return f"{number:.2f}"
    elif number < 100000:  # Less than 1 lakh
        return f"{number/1000:.2f} thousand"
    elif number < 10000000:  # Less than 1 crore
        return f"{number/100000:.2f} lakh"
    else:  # 1 crore or more
        return f"{number/10000000:.2f} crore"

st.write("### 📊 Results")
st.write(f"💰 **Total Amount Invested** ₹{format_indian_currency(total_invested)} ({get_abbreviated_amount(total_invested)})")
st.write(f"📈 **Future Value of Investment:** ₹{format_indian_currency(future_value)} ({get_abbreviated_amount(future_value)})")
st.write(f"📊 **Total Gain:** ₹{format_indian_currency(total_gain)} ({get_abbreviated_amount(total_gain)})")

# Calculate years and investment values
years = list(range(1, int(investment_period) + 1))
invested_values = [monthly_investment * 12 * y for y in years]

investment_growth = []
for y in years:
    months_y = y * 12
    future_val = monthly_investment * (((1 + monthly_rate)**months_y - 1) / monthly_rate) * (1 + monthly_rate)
    investment_growth.append(future_val)

st.write("### 📈 Investment Growth Visualizations")

# Create tabs for different visualizations
viz_tabs = st.tabs(["Growth Chart", "Contribution Breakdown", "Year-by-Year Growth", "Monthly vs Lump Sum"])

# Tab 1: Enhanced Line Chart (with annotations and better formatting)
with viz_tabs[0]:
    # Create a better line chart with Plotly
    fig = go.Figure()
    
    # Add investment line
    fig.add_trace(go.Scatter(
        x=years, 
        y=invested_values,
        mode='lines+markers',
        name='Amount Invested',
        line=dict(color='rgba(50, 168, 82, 0.8)', width=2),
        marker=dict(size=10)
    ))
    
    # Add growth line
    fig.add_trace(go.Scatter(
        x=years, 
        y=investment_growth,
        mode='lines+markers',
        name='Investment Value',
        line=dict(color='rgba(66, 133, 244, 0.8)', width=3),
        marker=dict(size=10),
        fill='tonexty',  # Fill the area between the two lines
        fillcolor='rgba(66, 133, 244, 0.1)'
    ))
    
    # Calculate the return percentage at the end
    final_return_pct = (investment_growth[-1] / invested_values[-1] - 1) * 100
    
    # Add annotations for the final values
    fig.add_annotation(
        x=years[-1],
        y=investment_growth[-1],
        text=f"₹{format_indian_currency(investment_growth[-1])} ({get_abbreviated_amount(investment_growth[-1])})",
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )
    
    fig.add_annotation(
        x=years[-1],
        y=invested_values[-1],
        text=f"₹{format_indian_currency(invested_values[-1])} ({get_abbreviated_amount(invested_values[-1])})",
        showarrow=True,
        arrowhead=1,
        ax=-40,
        ay=30
    )
    
    # Add annotation for return percentage
    fig.add_annotation(
        x=years[-1] * 0.75,
        y=investment_growth[-1] * 0.5,
        text=f"Total Return: {final_return_pct:.1f}%",
        showarrow=False,
        font=dict(size=14, color="green"),
        bordercolor="green",
        bgcolor="white",
        borderwidth=1,
        borderpad=4
    )
    
    # Layout improvements
    fig.update_layout(
        title="Investment Growth Over Time",
        xaxis_title="Year",
        yaxis_title="Amount (₹)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
        height=500
    )
    
    # Add rupee symbol to y-axis
    fig.update_yaxes(tickprefix="₹")
    
    # Show the plotly chart
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Pie chart showing principal vs. interest
with viz_tabs[1]:
    # Create data for pie chart
    final_investment = invested_values[-1]
    final_value = investment_growth[-1]
    interest_earned = final_value - final_investment
    
    # Create two columns for the visualization
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Create pie chart
        fig = px.pie(
            values=[final_investment, interest_earned],
            names=['Principal Amount', 'Interest Earned'],
            title="Principal vs. Interest Breakdown",
            color_discrete_sequence=['rgb(50, 168, 82)', 'rgb(66, 133, 244)'],
            hole=0.4
        )
        
        # Add percentages
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hoverinfo='label+value+percent'
        )
        
        # Update layout
        fig.update_layout(height=400)
        
        # Show chart
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Show key metrics in a clean format
        st.write("### Contribution Analysis")
        st.metric(
            label="Principal Amount", 
            value=f"₹{format_indian_currency(final_investment)}",
            delta=f"{(final_investment/final_value*100):.1f}% of total"
        )
        st.metric(
            label="Interest Earned", 
            value=f"₹{format_indian_currency(interest_earned)}",
            delta=f"{(interest_earned/final_value*100):.1f}% of total",
            delta_color="normal"
        )
        st.write(f"**ROI:** {(interest_earned/final_investment*100):.2f}%")

# Tab 3: Year-by-year growth analysis
with viz_tabs[2]:
    # Calculate year-by-year growth rates
    yearly_growth_rates = []
    yearly_additions = []
    
    for i in range(len(years)):
        if i == 0:
            yearly_growth = investment_growth[i] - invested_values[i]
            growth_rate = (yearly_growth / invested_values[i]) * 100
        else:
            yearly_investment = invested_values[i] - invested_values[i-1]
            yearly_growth = investment_growth[i] - investment_growth[i-1]
            yearly_addition = yearly_growth - yearly_investment
            yearly_additions.append(yearly_addition)
            growth_rate = (yearly_addition / investment_growth[i-1]) * 100
        
        if i > 0:  # Skip first year for growth rate calculation
            yearly_growth_rates.append(growth_rate)
    
    # Create a bar chart for growth contribution
    year_labels = [f"Year {y}" for y in years[1:]]  # Skip first year
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bars for yearly interest additions
    fig.add_trace(
        go.Bar(
            x=year_labels,
            y=yearly_additions,
            name="Interest Earned",
            marker_color='rgba(66, 133, 244, 0.8)'
        )
    )
    
    # Add line for growth rate
    fig.add_trace(
        go.Scatter(
            x=year_labels,
            y=yearly_growth_rates,
            name="Growth Rate (%)",
            mode='lines+markers',
            marker=dict(size=8, color='rgba(255, 112, 67, 1)'),
            line=dict(width=2, color='rgba(255, 112, 67, 1)')
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title="Year-by-Year Interest Contribution",
        height=500,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Interest Earned (₹)", secondary_y=False)
    fig.update_yaxes(title_text="Growth Rate (%)", secondary_y=True)
    
    # Show the figure
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: SIP vs Lump Sum comparison
with viz_tabs[3]:
    # Calculate equivalent lump sum amount (present value of all SIP investments)
    # This is a simplified calculation for comparison
    lump_sum_amount = monthly_investment * total_payments / (1 + annual_returns/100)**(investment_period/2)
    
    # Calculate lump sum growth
    lump_sum_growth = [lump_sum_amount * (1 + annual_returns/100)**(y) for y in years]
    
    # Create comparison chart
    fig = go.Figure()
    
    # Add SIP investment line
    fig.add_trace(go.Scatter(
        x=years, 
        y=investment_growth,
        mode='lines',
        name='SIP Investment',
        line=dict(color='rgba(66, 133, 244, 0.8)', width=3)
    ))
    
    # Add lump sum investment line
    fig.add_trace(go.Scatter(
        x=years, 
        y=lump_sum_growth,
        mode='lines',
        name='Equivalent Lump Sum',
        line=dict(color='rgba(255, 112, 67, 0.8)', width=3)
    ))
    
    # Layout improvements
    fig.update_layout(
        title="SIP vs Lump Sum Comparison",
        xaxis_title="Year",
        yaxis_title="Amount (₹)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
        height=500
    )
    
    # Add rupee symbol to y-axis
    fig.update_yaxes(tickprefix="₹")
    
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation
    st.info(
        """
        **SIP vs Lump Sum Comparison:**
        - The SIP approach involves investing ₹{} monthly over {} years.
        - The equivalent lump sum amount (₹{}) is the discounted present value of all SIP payments.
        - This comparison assumes the same annual return of {}% for both approaches.
        - SIP benefits from rupee-cost averaging in fluctuating markets, which isn't reflected in this theoretical model.
        """.format(
            format_indian_currency(monthly_investment),
            int(investment_period),
            format_indian_currency(lump_sum_amount),
            annual_returns
        )
    )

st.write("### Investment Data Table")

table_data = []
for y in years:
    invested = monthly_investment * 12 * y
    months_y = y * 12
    future_val = monthly_investment * (((1 + monthly_rate)**months_y - 1) / monthly_rate) * (1 + monthly_rate)
    table_data.append({"Year": y, "Invested Amount": format_indian_currency(invested), "Investment Value": format_indian_currency(future_val)})

df_table = pd.DataFrame(table_data)
df_table = df_table.reset_index(drop=True)
st.write("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.dataframe(df_table, use_container_width=True)
st.write("</div>", unsafe_allow_html=True)

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