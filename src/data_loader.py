import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_and_clean_data(self):
        self.df = pd.read_excel(self.file_path, engine='openpyxl')
        self.df = self.df.dropna()
        self.df = self.df.rename(columns={
            'Strike': 'Strike', 'IVM': 'ImpliedVolatility',
        })
        self.df['ImpliedVolatility'] = self.df['ImpliedVolatility'].astype(float) / 100
        self.df["ExpirationDate"] = self.df["Ticker"].apply(self._parse_ticker_to_date)
        
        unique_maturities = sorted(self.df['ExpirationDate'].unique())
        forward_prices = [449.42, 450.32, 451.47, 454.07, 457.71]
        maturity_to_forward = {maturity: forward_prices[i] for i, maturity in enumerate(unique_maturities)}
        self.df['IFwd'] = self.df['ExpirationDate'].map(maturity_to_forward)
        
        return self.df

    def _parse_ticker_to_date(self, ticker):
        parts = ticker.split()
        if len(parts) < 3:
            return None
        date_part = parts[1]
        try:
            expiry_date = datetime.strptime(date_part, "%m/%d/%y")
            return expiry_date
        except ValueError:
            return None
