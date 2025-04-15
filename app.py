import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 銘柄リスト
tickers = ["AAPL", "GOOGL", "MSFT"]

# 今日と1年前の日付を設定
today = datetime.today()
start_date = today - relativedelta(years=1)

# 四半期ごとの日付（3, 6, 9, 12ヶ月前）
quarter_dates = {
    "3 Months Ago": today - relativedelta(months=3),
    "6 Months Ago": today - relativedelta(months=6),
    "9 Months Ago": today - relativedelta(months=9),
    "12 Months Ago": today - relativedelta(months=12)
}

# 結果を保存する DataFrame（行：銘柄, 列：各時点）
results = pd.DataFrame(index=tickers, columns=quarter_dates.keys())

for ticker in tickers:
    df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    if df.empty:
        continue
    # 最新の終値を現在の価格として取得（float型に変換）
    current_price = float(df["Close"].iloc[-1])
    for label, date in quarter_dates.items():
        try:
            price = float(df.loc[:date.strftime('%Y-%m-%d')]["Close"].iloc[-1])
            change = (price / current_price - 1) * 100
            results.loc[ticker, label] = change
        except Exception as e:
            results.loc[ticker, label] = None

results = results.astype(float)
styled_df = results.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.2f}%")

st.markdown(styled_df.to_html(), unsafe_allow_html=True)
