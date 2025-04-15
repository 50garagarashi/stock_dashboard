"""
This application downloads stock price data for selected tickers (AAPL, GOOGL, MSFT) from Yahoo Finance over the past year.
It calculates the percentage change in price relative to today's closing price for specified past dates (3, 6, 9, and 12 months ago).
Today's closing price is included as a reference.
The results are displayed in a styled table with fixed background colors: green for positive percentage changes and red for negative changes.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Set the page configuration
st.set_page_config(
    page_title='Stock Price Change Dashboard',
    page_icon=':signal_strength:',
)

# App title
st.title("Stock Price Change Dashboard")

# Ticker symbols
tickers = ["AAPL", "GOOGL", "MSFT"]

# Set today's date and start date (1 year ago)
today = datetime.today()
start_date = today - relativedelta(years=1)

# Define past dates; keys are formatted as actual date strings (YYYY-MM-DD)
past_dates = {
    (today - relativedelta(months=3)).strftime('%Y-%m-%d'): today - relativedelta(months=3),
    (today - relativedelta(months=6)).strftime('%Y-%m-%d'): today - relativedelta(months=6),
    (today - relativedelta(months=9)).strftime('%Y-%m-%d'): today - relativedelta(months=9),
    (today - relativedelta(months=12)).strftime('%Y-%m-%d'): today - relativedelta(months=12)
}

# Prepare DataFrame with columns: "Today" plus the past dates as keys
columns = ["Today"] + list(past_dates.keys())
results = pd.DataFrame(index=tickers, columns=columns)

for ticker in tickers:
    # Download data from start_date to today
    df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    if df.empty:
        continue
    # Get today's closing price and store it in the "Today" column
    current_price = float(df["Close"].iloc[-1].item())
    results.loc[ticker, "Today"] = current_price
    # Calculate percentage change for each past date relative to today's price
    for date_label, date in past_dates.items():
        try:
            # Get the last available closing price on or before the specified date
            price = float(df.loc[:date.strftime('%Y-%m-%d')]["Close"].iloc[-1].item())
            change = (price / current_price - 1) * 100
            results.loc[ticker, date_label] = change
        except Exception as e:
            results.loc[ticker, date_label] = None

results = results.astype(float)

# Define custom formatting: "Today" displays as price and others as percentage values.
format_dict = {col: "{:.2f}%" for col in results.columns if col != "Today"}
format_dict["Today"] = "{:.2f}"

# Fix color scale for percentage changes:
# 全体での絶対値の最大値を求め、それを -max_abs ~ +max_abs の範囲に設定することで、0を中心に色付けする
change_columns = results.columns.drop("Today")
max_abs = results[change_columns].abs().max().max()

# Pandas のバージョン互換のため、center は使用せず vmin/vmax 固定スケールで色付け
styled_df = (
    results.style
    .format(format_dict)
    .background_gradient(cmap='RdYlGn', subset=change_columns, vmin=-max_abs, vmax=max_abs)
)

st.markdown(styled_df.to_html(), unsafe_allow_html=True)
