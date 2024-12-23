import pandas as pd
import os

def validate_csv_data(file_path):
    """
    Validerer, om CSV-data er gyldige.
    """
    if not os.path.exists(file_path):
        print(f"Fejl: Filen '{file_path}' eksisterer ikke.")
        return False

    try:
        df = pd.read_csv(file_path)
        required_columns = {'time', 'open', 'high', 'low', 'close'}
        if not required_columns.issubset(df.columns):
            print(f"Fejl: Filen '{file_path}' mangler nødvendige kolonner: {required_columns}.")
            return False
        return True
    except Exception as e:
        print(f"Fejl ved læsning af '{file_path}': {e}")
        return False


def load_and_clean_data(file_path):
        """
        Læs og rengør data fra en CSV-fil.

        Args:
            file_path (str): Stien til CSV-filen.

        Returns:
            pd.DataFrame: Det rensede DataFrame med tradingdata.
        """
        try:
            # Læs data fra CSV
            df = pd.read_csv(file_path)

            # Tjekker, at de nødvendige kolonner eksisterer
            required_columns = {'time', 'open', 'high', 'low', 'close'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Filen '{file_path}' mangler nødvendige kolonner: {required_columns}")

            # Konverter 'time'-kolonnen til datetime
            df['time'] = pd.to_datetime(df['time'], errors='coerce')

            # Sørg for, at de numeriske kolonner har korrekt datatype
            for col in ['open', 'high', 'low', 'close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Håndter manglende værdier
            if df[['open', 'high', 'low', 'close']].isnull().any().any():
                print(f"Advarsel: Manglende værdier fundet i '{file_path}'. Udfylder manglende værdier...")
                df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].fillna(method='ffill')
                df = df.dropna()  # Fjern evt. resterende rækker med NaN

            # Sorter data efter tid
            df.sort_values(by='time', inplace=True)
            df.reset_index(drop=True, inplace=True)

            return df

        except Exception as e:
            print(f"Fejl ved indlæsning og rengøring af data fra '{file_path}': {e}")
            return None