import yfinance as yf
import pandas as pd

def get_history(ticker: str, start_date: str, end_date: str):
    history = yf.Ticker(ticker).history(start=start_date, end=end_date)
    history = history.reset_index()
    history["Date"] = pd.to_datetime(history["Date"]).dt.strftime("%Y-%m-%d")

    return history