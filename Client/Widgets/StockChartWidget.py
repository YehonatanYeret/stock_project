import os
from PySide6.QtCore import Qt, QDate
import pandas as pd
import requests
from lightweight_charts.widgets import QtChart  # Use the QtChart widget for embedding
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

class StockChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = os.environ.get('POLYGON')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Create the embedded chart using QtChart
        self.chart = QtChart(self)

        # Set size policy to expanding so it stays large
        self.chart.get_webview().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set a minimum size to ensure it's large enough initially
        self.chart.get_webview().setMinimumSize(800, 400)

        # Add the chart at the bottom with stretch
        layout.addWidget(self.chart.get_webview(), stretch=1)

        self.setLayout(layout)

    def fetch_stock_data(self, ticker, start_date, end_date):
        """Fetch stock data from Polygon.io API"""
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={self.api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

            data = response.json().get('results', [])
            df = pd.DataFrame(data)

            if not df.empty:
                df['date'] = pd.to_datetime(df['t'], unit='ms')
                df = df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
                return df[['date', 'open', 'high', 'low', 'close', 'volume']]
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock data: {e}")
        
        return None

    def calculate_sma(self, df, period=50):
        """Calculate Simple Moving Average"""
        if df is not None and 'close' in df:
            sma = df['close'].rolling(window=period).mean()
            return pd.DataFrame({'time': df['date'], f'SMA {period}': sma}).dropna()
        return None

    def fetch_and_display_chart(self, ticker, start_date, end_date):
        """Fetch stock data and update the chart"""
        df = self.fetch_stock_data(ticker, start_date, end_date)
        
        if df is not None:
            self.chart.set(df)  # Set new data
            
            sma_data = self.calculate_sma(df, period=50)
            if sma_data is not None:
                line = self.chart.create_line('SMA 50')
                line.set(sma_data)
            
            self.chart.get_webview().update()
