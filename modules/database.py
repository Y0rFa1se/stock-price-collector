import pymysql
import os

def get_db_connection():
    connection = pymysql.connect(
        host=os.getenv("HOST"),
        user="root",
        password=os.getenv("PASSWORD"),
        database="mysql",
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS stock_prices")
        connection.commit()

    connection.select_db("stock_prices")
    
    return connection

def db_init(tickers: list):
    conn = get_db_connection()
    c = conn.cursor()
    
    for ticker in tickers:
        if ticker.startswith("^"):
            ticker = ticker[1:]

        ticker += "_prices"

        c.execute(f"""CREATE TABLE IF NOT EXISTS {ticker} (
                        idx INT AUTO_INCREMENT PRIMARY KEY,
                        date DATE,
                        open DECIMAL(20, 10),
                        high DECIMAL(20, 10),
                        low DECIMAL(20, 10),
                        close DECIMAL(20, 10),
                        volume BIGINT,
                        dividends DECIMAL(20, 10),
                        stock_splits DECIMAL(20, 10)
                        )""")
        
    conn.commit()
    conn.close()

def get_last_date(ticker: str):
    if ticker.startswith("^"):
        ticker = ticker[1:]

    ticker += "_prices"

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute(f"SELECT date FROM {ticker} ORDER BY idx DESC LIMIT 1")
    last_date = c.fetchone()
    
    conn.close()
    
    if last_date:
        return str(last_date['date'])
    else:
        return None

def insert_data(ticker: str, data) -> bool:
    if ticker.startswith("^"):
        ticker = ticker[1:]

    ticker += "_prices"

    if data.empty:
        return False

    conn = get_db_connection()
    c = conn.cursor()

    for index, row in data.iterrows():
        c.execute(f"""INSERT INTO {ticker} (date, open, high, low, close, volume, dividends, stock_splits) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (row["Date"], row["Open"], row["High"], row["Low"], row["Close"], row["Volume"], row["Dividends"], row["Stock Splits"]))
        
    conn.commit()
    conn.close()

    return True
