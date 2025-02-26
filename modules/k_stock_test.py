from pykrx import stock

kospi_tickers = stock.get_market_ticker_list(market="KOSPI")
print(kospi_tickers)
