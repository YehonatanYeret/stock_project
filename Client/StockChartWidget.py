from PySide6.QtCore import Qt
import pandas as pd
from lightweight_charts.widgets import QtChart  # Use QtChart for embedding
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

class StockChartWidget(QWidget):
    def __init__(self, parent=None):
        """
        StockChartWidget initializes an empty chart and waits for data.
        """
        super().__init__(parent)
        self.chart = None  # Placeholder for chart
        self.data = None  # Placeholder for stock data
        self.init_ui()

    def init_ui(self):
        """Initialize the UI with an empty chart"""
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

    def process_data(self, data):
        """Process raw stock data into a DataFrame"""
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)

            # Ensure required columns exist
            required_columns = {'t', 'o', 'h', 'l', 'c', 'v'}
            if not required_columns.issubset(df.columns):
                print("⚠️ Error: Missing required columns in stock data!")
                return None

            df['date'] = pd.to_datetime(df['t'], unit='ms')  # Convert timestamp
            df = df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
            return df[['date', 'open', 'high', 'low', 'close', 'volume']]
        return None

    def calculate_sma(self, df, period=50):
        """Calculate Simple Moving Average (SMA)"""
        if df is not None and 'close' in df:
            sma = df['close'].rolling(window=period).mean()
            return pd.DataFrame({'time': df['date'], f'SMA {period}': sma}).dropna()
        return None

    def display_chart(self):
        """Render the chart with existing stock data"""
        if self.data is not None:
            self.chart.set(self.data)  # Set new data
            
            # Compute and display SMA line
            sma_data = self.calculate_sma(self.data, period=50)
            if sma_data is not None:
                line = self.chart.create_line('SMA 50')
                line.set(sma_data)

            self.chart.get_webview().update()

    def update_chart(self, ticker, start_date, end_date, data):
        """
        Update the chart dynamically with new stock data.

        :param ticker: Stock symbol
        :param start_date: Start date
        :param end_date: End date
        :param data: Stock data in list format
        """
        print(f"📈 Updating chart for {ticker} from {start_date} to {end_date}")

        self.data = self.process_data(data)  # Convert to DataFrame
        if self.data is not None:
            # self.auto_zoom_chart()
            self.chart.set_visible_range(start_date, end_date)  # Set visible range
            self.display_chart()  # Display updated chart
        else:
            print("❌ Error: Unable to process stock data.")


    def clear_chart(self):
        """Clears the chart for new data."""
        self.chart.clear()
        print("🧹 Chart cleared.")
