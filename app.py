from datetime import datetime, timedelta
import streamlit as st
from main import stock_analysis
import plotly.io as pio
import streamlit.components.v1 as components


def run():
    st.title("📈 Stock Analysis Tool")

    # User input for stock symbol
    stock = st.text_input("Enter Stock Symbol", "AAPL")

    # User input for months of data
    months = st.number_input(
        "Months of Data", min_value=1, max_value=60, value=6)

    # Calculate the allowed date range
    max_date = datetime.today()
    # Approximate month length as 30 days
    min_date = max_date - timedelta(days=months*30)

    # User input for Buy Date with restriction for future dates and past dates
    buy_date = st.date_input(
        "Buy Date", max_value=max_date, min_value=min_date)

    # Check if the selected date is a Saturday or Sunday
    if buy_date.weekday() == 5:  # Saturday
        st.warning("You cannot select a Saturday. Please choose a weekday.")
        # Adjust to the previous Friday
        buy_date = buy_date - timedelta(days=1)
    elif buy_date.weekday() == 6:  # Sunday
        st.warning("You cannot select a Sunday. Please choose a weekday.")
        # Adjust to the previous Friday
        buy_date = buy_date - timedelta(days=2)

    # Button to trigger the analysis
    if st.button("Show Analysis"):
        # Call the stock analysis function (assuming you have defined it)
        st.write(f"Performing stock analysis for {
            stock} starting on {buy_date.strftime('%Y-%m-%d')} for {months} months.")
        fig = stock_analysis(stock, buy_date.strftime(
            '%Y-%m-%d %H:%M:%S'), months)

        graph_html = pio.to_html(fig, full_html=False)

        # Streamlit App
        st.title("Plotly Graph in Streamlit")

        # Check if graph_html exists and render it
        if graph_html:
            components.html(graph_html, width=1200, height=600)


# Run the app
if __name__ == "__main__":
    run()
