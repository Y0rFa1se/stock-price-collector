import sqlite3

def db_init(tickers: list):
    conn = sqlite3.connect('../../files/stock.db')
    conn.execute("PRAGMA journal_mode=WAL;")

    c = conn.cursor()
    
    for ticker in tickers:
        if ticker.startswith("^"):
            ticker = ticker[1:]

        ticker += "_prices"

        c.execute(f"""CREATE TABLE IF NOT EXISTS {ticker} (
                    idx INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    dividends REAL,
                    stock_splits REAL
                    )""")
        
    conn.commit()
    conn.close()

def get_last_date(ticker: str):
    if ticker.startswith("^"):
        ticker = ticker[1:]

    ticker += "_prices"

    conn = sqlite3.connect('../../files/stock.db')
    conn.execute("PRAGMA journal_mode=WAL;")
    
    c = conn.cursor()
    
    c.execute(f"SELECT date FROM {ticker} ORDER BY idx DESC LIMIT 1")
    last_date = c.fetchone()
    
    conn.close()
    
    if last_date:
        return last_date[0]
    else:
        return None
    
def insert_data(ticker: str, data) -> bool:
    if ticker.startswith("^"):
        ticker = ticker[1:]

    ticker += "_prices"

    if data.empty:

        return False

    conn = sqlite3.connect('../../files/stock.db')
    conn.execute("PRAGMA journal_mode=WAL;")
    
    c = conn.cursor()

    for index, row in data.iterrows():
        c.execute(f"INSERT INTO {ticker} (date, open, high, low, close, volume, dividends, stock_splits) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (row["Date"], row["Open"], row["High"], row["Low"], row["Close"], row["Volume"], row["Dividends"], row["Stock Splits"]))
        
    conn.commit()
    conn.close()

    return True