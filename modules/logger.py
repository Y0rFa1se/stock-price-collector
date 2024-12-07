from os import makedirs

def log_init():
    makedirs("logs", exist_ok=True)

def log(msg: str, date: str):
    with open(f"logs/stock_{date}.log", "a") as f:
        f.write(msg)