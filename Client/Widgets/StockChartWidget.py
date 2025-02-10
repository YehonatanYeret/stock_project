from PySide6.QtCore import Qt
import pandas as pd
from lightweight_charts.widgets import QtChart  # Use the QtChart widget for embedding
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

class StockChartWidget(QWidget):
    def __init__(self, ticker, start_date, end_date, data, parent=None):
        """
        StockChartWidget receives pre-fetched data and simply renders the chart.
        
        :param ticker: Stock ticker symbol (e.g., "AAPL")
        :param start_date: Start date (YYYY-MM-DD)
        :param end_date: End date (YYYY-MM-DD)
        :param data: Pre-fetched stock data in DataFrame format
        """
        super().__init__(parent)
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.process_data(data)  # Process data before rendering
        self.init_ui()

    def init_ui(self):
        """Initialize the chart UI and display data"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Create the embedded chart
        self.chart = QtChart(self)

        # Set size policy for auto resizing
        self.chart.get_webview().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart.get_webview().setMinimumSize(800, 400)

        # Add the chart widget
        layout.addWidget(self.chart.get_webview(), stretch=1)

        self.setLayout(layout)

        # Display chart with given data
        self.display_chart()

    def process_data(self, data):
        """Process raw stock data into a usable DataFrame"""
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['t'], unit='ms')  # Convert timestamp
            df = df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
            return df[['date', 'open', 'high', 'low', 'close', 'volume']]
        return None

    def calculate_sma(self, df, period=50):
        """Calculate Simple Moving Average"""
        if df is not None and 'close' in df:
            sma = df['close'].rolling(window=period).mean()
            return pd.DataFrame({'time': df['date'], f'SMA {period}': sma}).dropna()
        return None

    def display_chart(self):
        """Render the chart with stock data"""
        if self.data is not None:
            self.chart.set(self.data)  # Set new data
            
            # Compute and display SMA line
            sma_data = self.calculate_sma(self.data, period=50)
            if sma_data is not None:
                line = self.chart.create_line('SMA 50')
                line.set(sma_data)

            self.chart.get_webview().update()
