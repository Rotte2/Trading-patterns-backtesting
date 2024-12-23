import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# Liste over tickers (Apple, Meta, SPY, Tesla, Palantir)
tickers = ['AAPL', 'META', 'SPY', 'TSLA', 'PLTR']

# Beregn start- og slutdato for de seneste 6 måneder
end_date = datetime.today()
start_date = end_date - timedelta(days=6 * 30)  # Ca. 6 måneder tilbage

# Opret mappe til at gemme data
data_directory = "data_stocks"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Hent data og gem i det rigtige format
for ticker in tickers:
    print(f"Henter data for {ticker}...")
    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1d')

    if data.empty:
        print(f"Ingen data fundet for {ticker}.")
        continue

    # Omformater data til det ønskede format
    data.reset_index(inplace=True)
    data.rename(columns={
        'Date': 'time',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close'
    }, inplace=True)
    data = data[['time', 'open', 'high', 'low', 'close']]  # Behold kun nødvendige kolonner

    # Gem data som CSV-fil i "data_stocks"-mappen
    file_name = os.path.join(data_directory, f"{ticker}_6_months.csv")
    data.to_csv(file_name, index=False)
    print(f"{file_name} gemt.")
