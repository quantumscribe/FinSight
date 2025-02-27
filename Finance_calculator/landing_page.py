import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


# --- Hero Section ---
st.markdown(
    """
    <div style="text-align: center; padding: 4rem 0;">
        <h1 style="font-size: 3rem; font-weight: bold; margin-bottom: 1rem;">Financial Freedom Starts Here</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem;">Empower your financial decisions.</p>
        <a href="#calculators" style="background-color: #007bff; color: white; padding: 1rem 2rem; border-radius: 5px; text-decoration: none; font-size: 1.2rem;">Explore Calculators</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- About Us Section (Optional) ---
st.markdown("---")
st.markdown(
    """
    <div style="padding: 2rem;">
        <h2>About Us</h2>
        <p>We are dedicated to providing you with the tools and information you need to take control of your finances. Our mission is to simplify complex financial concepts and make sound financial planning accessible to everyone.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Calculators Section ---
st.markdown("---")
st.markdown("<h2 id='calculators'>Calculators</h2>", unsafe_allow_html=True)

# Grid Layout for Calculators
num_cols = 3
calculator_data = [
    {"title": "Investment Growth", "description": "Calculate future value of investments.", "link": "#investment"},
    {"title": "Loan Calculator", "description": "Calculate monthly loan payments.", "link": "#loan"},
    {"title": "Retirement Planner", "description": "Plan for your retirement savings.", "link": "#retirement"},
    {"title": "Budget Planner", "description": "Create and manage your budget.", "link": "#budget"},
    {"title": "Savings Goal", "description": "Calculate how much to save.", "link": "#savings"},
    {"title": "Compound Interest", "description": "See the power of compounding.", "link": "#compound"},
]

cols = st.columns(num_cols)

for i, calculator in enumerate(calculator_data):
    col_index = i % num_cols
    with cols[col_index]:
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; border-radius: 5px;">
                <h3>{calculator['title']}</h3>
                <p>{calculator['description']}</p>
                <a href="{calculator['link']}" style="color: #007bff; text-decoration: none;">Go to Calculator</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 1rem; background-color: #333; color: white;">
        &copy; 2025 FinSight. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)

# --- JavaScript for showing/hiding calculators ---
st.markdown(
    """
    <script>
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const calculatorSections = document.querySelectorAll('[id]');

                calculatorSections.forEach(section => {
                    if (section.id !== targetId && section.id !== 'calculators') {
                        section.style.display = 'none';
                    }
                });

                targetElement.style.display = 'block';
            }
        });
    });
    </script>
    """,
    unsafe_allow_html=True,
)