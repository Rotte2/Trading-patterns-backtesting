from strategies.engulfing_strategy import EngulfingStrategy
from utils.data_utils import validate_csv_data, load_and_clean_data
from utils.plot_utils import plot_signals
import os
from time import sleep


def run_simulation(ticker, strategy, data_directory="data_stocks"):
    """
    Kører simuleringen for det angivne ticker-symbol og en valgt strategi.

    Args:
        ticker (str): Ticker-symbol for aktien (f.eks. 'AAPL').
        strategy (object): Strategiobjekt, der implementerer en 'generate_signal'-metode.
        data_directory (str): Mappe, hvor datafilerne er gemt.
    """
    file_path = os.path.join(data_directory, f"{ticker}_6_months.csv")

    # Valider og indlæs data
    if not validate_csv_data(file_path):
        return

    df = load_and_clean_data(file_path)
    if df is None:
        print(f"Fejl: Kunne ikke indlæse data for '{ticker}'.")
        return

    print(f"Kører simulering for {ticker} med strategien {strategy.__class__.__name__}...")

    position = None
    signals = []

    # Iterér gennem data og anvend strategien
    for index in range(1, len(df)):
        candle = {
            'open': df['open'].iloc[index],
            'high': df['high'].iloc[index],
            'low': df['low'].iloc[index],
            'close': df['close'].iloc[index],
            'previous_open': df['open'].iloc[index - 1],
            'previous_high': df['high'].iloc[index - 1],
            'previous_low': df['low'].iloc[index - 1],
            'previous_close': df['close'].iloc[index - 1],
        }

        signal = strategy.generate_signal(candle)
        signals.append(signal)

        # Håndter signaler og positioner
        if signal == 'buy' and position is None:
            print(f"KØB-signal fundet på {df['time'].iloc[index]} @ {df['close'].iloc[index]}")
            position = 'long'

        elif signal == 'sell' and position is None:
            print(f"SÆLG-signal fundet på {df['time'].iloc[index]} @ {df['close'].iloc[index]}")
            position = 'short'

        if position == 'long' and signal == 'sell':
            print(f"LUKKER LONG-position på {df['time'].iloc[index]} @ {df['close'].iloc[index]}")
            position = None

        elif position == 'short' and signal == 'buy':
            print(f"LUKKER SHORT-position på {df['time'].iloc[index]} @ {df['close'].iloc[index]}")
            position = None

        sleep(0.1)

    print("Simulering afsluttet.")
    plot_signals(df, signals)


if __name__ == '__main__':
    data_directory = "data_stocks"
    if not os.path.exists(data_directory):
        print(f"Fejl: Mappen '{data_directory}' eksisterer ikke. Opret denne mappe og tilføj CSV-filer.")
    else:
        ticker = input("Angiv ticker-symbol (f.eks. AAPL, META, SPY): ").upper()
        strategy = EngulfingStrategy()  # Du kan vælge andre strategier her
        run_simulation(ticker, strategy, data_directory=data_directory)
