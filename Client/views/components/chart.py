import pandas as pd
from PySide6.QtCore import QDate
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from lightweight_charts.widgets import QtChart


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
        print("⚠️ Error: Invalid stock data format!", data)
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
        :param start_date: Start date as a string in "yyyy-MM-dd" format
        :param end_date: End date as a string in "yyyy-MM-dd" format
        :param data: Stock data in list format
        """

        # self.clear_chart()  # Clear the chart before updating
        self.data = self.process_data(data)  # Convert to DataFrame
        if self.data is not None:
            # Convert string dates to QDate objects
            # start_date_qdate = QDate.fromString(start_date, "yyyy-MM-dd")
            # end_date_qdate = QDate.fromString(end_date, "yyyy-MM-dd")
            #
            # # Convert QDate objects to timestamps (milliseconds)
            # start_dt = pd.to_datetime(start_date_qdate.toString("yyyy-MM-dd"))
            # end_dt = pd.to_datetime(end_date_qdate.toString("yyyy-MM-dd"))
            #
            # start_ts = int(start_dt.timestamp() * 1000)
            # end_ts = int(end_dt.timestamp() * 1000)

            # Set visible range using the converted timestamps
            # self.chart.set_visible_range(start_ts, end_ts)
            
            self.display_chart()  # Display updated chart

            self.chart.get_webview().page().runJavaScript("chart.timeScale().fitContent();")


        else:
            print("❌ Error: Unable to process stock data.")

    def clear_chart(self):
        """Clears the chart for new data."""
        self.chart.set(pd.DataFrame())  # Set an empty list to clear the chart data
        self.chart.get_webview().update()  # Update the webview to reflect changes
        print("🧹 Chart cleared.")
