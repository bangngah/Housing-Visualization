import streamlit as st
import matplotlib.pyplot as plt  # Added import for plotting
from matplotlib.figure import Figure  # Added import for plotting
import seaborn as sns
import plost 
import pandas as pd
import plotly.express as px
import numpy as np

def calculate_mortgage_details(principal, years, rate, property_tax_rate, insurance):
    monthly_rate = rate / 100 / 12
    n_payments = years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)

    # Monthly property tax and insurance
    monthly_property_tax = (principal * property_tax_rate / 100) / 12
    monthly_payment_with_tax_insurance = monthly_payment + monthly_property_tax + insurance

    # Total costs
    total_interest = monthly_payment * n_payments - principal
    total_property_tax = monthly_property_tax * n_payments
    total_insurance = insurance * n_payments
    total_cost = principal + total_interest + total_property_tax + total_insurance

    return monthly_payment_with_tax_insurance, total_cost, total_interest, total_property_tax, total_insurance


def show_data_page(df_property):

    # Mortgage Calculator Section
    st.subheader("Mortgage Calculator")
    col1, col2 = st.columns(2)

    with col1:
        home_price = st.number_input("Home Price ($)", min_value=0.0, value=300000.0, step=1000.0)
        down_payment = st.number_input("Down Payment Amount ($)", min_value=0.0, value=60000.0, step=1000.0)
        loan_term = st.selectbox("Loan Term (Years)", [10, 15, 30])  # Dropdown for loan term

    with col2:
        interest_rate = st.slider("Interest Rate % (Yearly)", min_value=1.0, max_value=20.0, value=3.0, step=0.1)  # Slider for interest rate
        property_tax_rate = st.slider("Property Tax Rate % (Yearly)", min_value=1.0, max_value=20.0, value=1.2, step=0.1)  # Slider for property tax rate
        home_insurance = st.number_input("Home Insurance ($ per Month)", min_value=0.0, value=50.0, step=10.0)

    if st.button('Calculate Mortgage'):
        principal = home_price - down_payment
        monthly_payment, total_cost, total_interest, total_property_tax, total_insurance = calculate_mortgage_details(
            principal, loan_term, interest_rate, property_tax_rate, home_insurance
        )
        st.write(f"Estimated Monthly Payment: ${monthly_payment:.2f}")
        st.write(f"Total Mortgage Cost over {loan_term} years: ${total_cost:.2f}")

        st.write("-----")

 # Donut Chart
        labels = ['Principal', 'Total Interest', 'Total Property Tax', 'Total Insurance']
        sizes = [principal, total_interest, total_property_tax, total_insurance]
        fig, ax = plt.subplots(figsize=(3, 2))  # Adjusted figure size
        ax.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%', startangle=140, wedgeprops=dict(width=0.3), textprops={'fontsize': 5})
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        st.write("Mortgage Cost Breakdown:")
        st.pyplot(fig)

# Main function or entry point
if __name__ == "__main__":
    # Sample data for demonstration
    df_property = pd.DataFrame({
        'monthly_rent': np.random.randint(500, 5000, 100),
        'rooms': np.random.randint(1, 6, 100)
    })
    
    show_data_page(df_property)