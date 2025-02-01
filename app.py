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

        graph_html = pio.to_html(fig, full_html=False,
                                 config={"responsive": True})

        # Streamlit App
        st.title(f"{stock}")

        # Custom CSS to make the chart scale down on mobile
        custom_css = """
            <style>
                .plot-container {
                    max-width: 100%;
                    margin: auto;
                    display: flex;
                    justify-content: center;
                }
                @media (max-width: 600px) {
                    .plot-container iframe {
                        width: 100% !important;
                        height: 300px !important;  /* Reduce height on small screens */
                    }
                }
            </style>
        """

        # Streamlit App
        st.title(f"{stock}")

        # Create a container for responsive design
        with st.container():
            st.write(
                "This graph is optimized for mobile screens and will resize automatically.")

            # Render custom CSS
            st.markdown(custom_css, unsafe_allow_html=True)

            # Wrap the graph in a div with class "plot-container"
            components.html(
                f'<div class="plot-container">{graph_html}</div>', height=600, width=1200)


# Run the app
if __name__ == "__main__":
    run()
