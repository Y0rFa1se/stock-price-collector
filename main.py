from time import sleep
from tqdm import tqdm
from dotenv import load_dotenv

from modules.calculate_date import today, next_day, date_iterator
from modules.database import db_init, get_last_date, insert_data
from modules.requests_prices import get_history
from modules.tickers import load_tickers
from modules.logger import log_init, log

load_dotenv()

log_init()

OLDEST_DATE = "1971-01-01"
TICKERS = load_tickers()

db_init(TICKERS)

TODAY = today()

for idx, ticker in tqdm(enumerate(TICKERS)):
    log(f"({idx+1}/{len(TICKERS)}) {ticker}\n", TODAY)

    date = get_last_date(ticker)
    if date:
        date = next_day(date)
    else:
        date = OLDEST_DATE

    for idx, (start_date, end_date) in enumerate(date_iterator(date, TODAY)):
        log(f"| {start_date} ~ {end_date} ", TODAY)
        data = get_history(ticker, start_date, end_date)
        
        response = insert_data(ticker, data)
        if response:
            log("O\n", TODAY)
        else:
            log("X\n", TODAY)
            
        sleep(3)

    log("\n", TODAY)
    sleep(3)

log("!!! Done !!!\n\n", TODAY)