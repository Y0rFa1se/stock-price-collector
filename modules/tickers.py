def load_tickers(file_path: str = "tickers.txt") -> list:
    with open(file_path, "r") as f:
        tickers = f.read().splitlines()
        
    return tickers
