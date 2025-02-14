import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import base64  # For background image
st.set_page_config(layout="wide", page_title="Personal Finance & Investment Hub")

# --- Helper function for background image ---
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
st.markdown(
    """
    <script>
    const links = document.querySelectorAll('a[href^="#"]'); // Select all links that start with #

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior

            const targetId = this.getAttribute('href').substring(1); // Get the target ID
            const targetElement = document.getElementById(targetId); // Get the target element

            if (targetElement) {
                targetElement.style.display = 'block'; // Show the target element
            }
        });
    });
    </script>
    """,
    unsafe_allow_html=True,
)


# --- Set background image (replace with your image path) ---
# set_background("your_background_image.jpg")  # Replace with actual path


# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Personal Finance & Investment Hub")

# --- Hero Section ---
st.markdown(
    """
    <div style="text-align: center; padding: 4rem 0;">  <h1 style="font-size: 3rem; font-weight: bold; margin-bottom: 1rem;">Financial Freedom Starts Here</h1>
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
num_cols = 3  # Number of columns in the grid
calculator_data = [  # List of dictionaries, each for a calculator
    {"title": "Investment Growth", "description": "Calculate future value of investments.", "link": "#investment"},
    {"title": "Loan Calculator", "description": "Calculate monthly loan payments.", "link": "#loan"},
    {"title": "Retirement Planner", "description": "Plan for your retirement savings.", "link": "#retirement"},
    {"title": "Budget Planner", "description": "Create and manage your budget.", "link": "#budget"},
    {"title": "Savings Goal", "description": "Calculate how much to save.", "link": "#savings"},
    {"title": "Compound Interest", "description": "See the power of compounding.", "link": "#compound"},
    # ... Add more calculators here ...
]

# Create the grid
cols = st.columns(num_cols)  # Create the columns

for i, calculator in enumerate(calculator_data):
    col_index = i % num_cols  # Calculate the column index
    with cols[col_index]:  # Place the calculator in the correct column
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; padding: 1rem; margin-bottom: 1rem; border-radius: 5px; background-color: rgba(255, 255, 255, 0.2);">
                <h3 style="color:white">{calculator['title']}</h3>
                <p style="color:white">{calculator['description']}</p>
                <a href="{calculator['link']}" style="color: #007bff; text-decoration: none;">Go to Calculator</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- Individual Calculator Sections (Hidden initially) ---
st.markdown("<div style='display: none;'>", unsafe_allow_html=True) # Start hidden div

# Investment Calculator
st.subheader("Investment Growth Calculator", key="investment")  # Add a key
# ... (Investment calculator code)

# Loan Calculator
st.subheader("Loan Calculator", key="loan")  # Add a key
# ... (Loan calculator code)

# ... (Add other calculator sections with unique keys)

st.markdown("</div>", unsafe_allow_html=True) # End hidden div
# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 1rem; background-color: rgba(0, 0, 0, 0.5); color: white;">  &copy; 2023 Your Finance App. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)