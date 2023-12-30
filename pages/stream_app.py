# Import necessary libraries
import numpy as np
import streamlit as st
import yfinance as yf
import plotly.express as px

# Set the title of the Streamlit app
st.title("Real-time Stock Dashboard")

# Create sidebar inputs for user interaction
# Input for stock ticker
ticker = st.sidebar.text_input("Ticker")
# Input for start date of data
start_date = st.sidebar.date_input("Start Date")
# Input for end date of data
end_date = st.sidebar.date_input("End Date")

# Conditional execution when a ticker symbol is provided
if ticker:
    # Download stock data using yfinance
    data = yf.download(ticker, start=start_date, end=end_date)

    # Check if the downloaded data is not empty
    if not data.empty:
        # Create a line plot of the adjusted closing prices using Plotly
        fig = px.line(data, x=data.index, y='Adj Close', title=ticker)
        st.plotly_chart(fig)
    else:
        # Display message if no data is available
        st.write("No data available for the given ticker and date range.")
else:
    # Prompt for ticker input if not provided
    st.write("Please enter a ticker symbol.")

# Create tabs for different data views
pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

# Pricing data tab
with pricing_data:
    st.header("Price Movements")
    # Calculate percentage change in adjusted close prices
    data2 = data
    data2["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace=True)  # Remove NaN values
    st.write(data2)
    # Calculate and display annual return
    annual_return = data2["% Change"].mean() * 252 * 100
    st.write('Annual Return is ', annual_return, "%")
    # Calculate and display standard deviation (volatility)
    stdev = np.std(data2["% Change"]) * np.sqrt(252)
    st.write("Standard Deviation is ", stdev * 100, "%")
    # Calculate and display risk-adjusted return
    st.write("Risk-Adjusted Return is ", annual_return / (stdev * 100))

# Fundamental data tab
api_key="DDTH51SAIK67KCNE"
with fundamental_data:
    st.write("Fundamental Data Display")

# News tab
with news:
    st.write("News Display")
