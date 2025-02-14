import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.title("CAGR Calculator")

st.write("### Input Data")

initial_investment = st.slider("Initial Investment Amount (₹)", min_value=1000, max_value=1000000, value=10000, step=1000)
final_investment = st.slider("Final Investment Amount (₹)", min_value=1000, max_value=10000000, value=20000, step=1000)  # Increased max_value
time_period = st.slider("Time Period (Years)", min_value=1, max_value=50, value=5, step=1)

# CAGR Calculation
if initial_investment <= 0 or time_period <= 0:
    st.error("Initial investment and time period must be greater than zero.")
else:
    cagr = ((final_investment / initial_investment) ** (1 / time_period) - 1) * 100

    st.write("### 📊 Results")
    st.write(f"📈 **CAGR:** {cagr:,.2f}%")

    # --- Visualizations ---
    st.write("### Visualizations")

    # 1. Investment Growth Over Time (Line Chart)
    years = np.arange(0, time_period + 1)
    investment_values = [initial_investment * (1 + cagr / 100) ** y for y in years]

    growth_df = pd.DataFrame({"Year": years, "Investment Value": investment_values})

    growth_chart = (
        alt.Chart(growth_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("Investment Value:Q", title="Amount (₹)"),
            tooltip=["Year", alt.Tooltip("Investment Value:Q", format=",.2f")],
        )
        .properties(title="Investment Growth Over Time")
        .interactive()
    )
    st.altair_chart(growth_chart, use_container_width=True)


    # 3. CAGR Interpretation Text
    st.write("### CAGR Interpretation")

    if cagr < 0 :
        st.write(f"The Compound Annual Growth Rate (CAGR) of {cagr:,.2f}% indicates a negative return on your investment over the specified period.")
    elif cagr < 5:
        st.write(f"The Compound Annual Growth Rate (CAGR) of {cagr:,.2f}% is considered low growth.")
    elif cagr < 10:
        st.write(f"The Compound Annual Growth Rate (CAGR) of {cagr:,.2f}% is considered moderate growth.")
    elif cagr < 15:
        st.write(f"The Compound Annual Growth Rate (CAGR) of {cagr:,.2f}% is considered good growth.")
    else:
        st.write(f"The Compound Annual Growth Rate (CAGR) of {cagr:,.2f}% is considered excellent growth.")