from time import sleep
from tqdm import tqdm

from modules.backup import backup_init, upload
from modules.calculate_date import today, date_iterator
from modules.database import db_init, get_last_date, insert_data
from modules.requests_prices import get_history
from modules.tickers import load_tickers
from modules.logger import log_init, log

log_init()

OLDEST_DATE = "1971-01-01"
TICKERS = load_tickers()

DRIVE = backup_init()
db_init(TICKERS)

TODAY = today()

for ticker in tqdm(TICKERS):
    log(ticker, TODAY)

    date = get_last_date(ticker)
    if not date:
        date = OLDEST_DATE

    log

    for idx, (start_date, end_date) in enumerate(date_iterator(date, TODAY)):
        log(f"{start_date} ~ {end_date}", TODAY)
        data = get_history(ticker, start_date, end_date)
        insert_data(ticker, data)
        sleep(3)

    upload(DRIVE, "stock.db", "stock_prices.db")
    log("\n", TODAY)
    sleep(3)