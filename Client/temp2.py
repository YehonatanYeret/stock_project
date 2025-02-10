# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDateEdit,
#     QSizePolicy, QSpacerItem, QApplication
# )
# from PySide6.QtCore import Qt, QDate
# import pandas as pd
# import requests
# from lightweight_charts.widgets import QtChart  # Use the QtChart widget for embedding
# import sys

# class StockChartWidget(QWidget):
#     def __init__(self, api_key):
#         super().__init__()
#         self.api_key = api_key
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()
#         layout.setAlignment(Qt.AlignTop)

#         # Ticker input
#         self.ticker_input = QLineEdit()
#         self.ticker_input.setPlaceholderText("Enter Ticker (e.g., AAPL)")
#         layout.addWidget(self.ticker_input)

#         # Start date input
#         self.start_date_input = QDateEdit()
#         self.start_date_input.setCalendarPopup(True)
#         self.start_date_input.setDate(QDate.currentDate().addYears(-1))
#         layout.addWidget(QLabel("Start Date:"))
#         layout.addWidget(self.start_date_input)

#         # End date input
#         self.end_date_input = QDateEdit()
#         self.end_date_input.setCalendarPopup(True)
#         self.end_date_input.setDate(QDate.currentDate())
#         layout.addWidget(QLabel("End Date:"))
#         layout.addWidget(self.end_date_input)

#         # Fetch button
#         self.fetch_button = QPushButton("Fetch Data")
#         self.fetch_button.clicked.connect(self.fetch_and_display_chart)
#         layout.addWidget(self.fetch_button)

#         # Spacer to push the chart to the bottom
#         layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

#         # Create the embedded chart using QtChart.
#         self.chart = QtChart(self)

#         # Set size policy to expanding so it stays large
#         self.chart.get_webview().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

#         # Set a minimum size to ensure it's large enough initially
#         self.chart.get_webview().setMinimumSize(800, 600)

#         # Add the chart at the bottom with stretch
#         layout.addWidget(self.chart.get_webview(), stretch=1)  # Ensures it occupies remaining space

#         self.setLayout(layout)

#     def fetch_stock_data(self, ticker, start_date, end_date):
#         url = (f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={self.api_key}")
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json().get('results', [])
#             df = pd.DataFrame(data)
#             if not df.empty:
#                 df['date'] = pd.to_datetime(df['t'], unit='ms')
#                 df = df.rename(columns={
#                     'o': 'open',
#                     'h': 'high', 
#                     'l': 'low', 
#                     'c': 'close',
#                     'v': 'volume'
#                 })
#                 return df[['date', 'open', 'high', 'low', 'close', 'volume']]
#         return None

#     def calculate_sma(self, df, period=50):
#         sma = df['close'].rolling(window=period).mean()
#         return pd.DataFrame({'time': df['date'], f'SMA {period}': sma}).dropna()

#     def fetch_and_display_chart(self):
#         ticker = self.ticker_input.text().upper()
#         start_date = self.start_date_input.date().toString("yyyy-MM-dd")
#         end_date = self.end_date_input.date().toString("yyyy-MM-dd")
#         if not ticker:
#             return

#         df = self.fetch_stock_data(ticker, start_date, end_date)
#         if df is not None:
#             # self.chart.clear()  # Clear previous data.
#             self.chart.set(df)  # Set new data.
#             # Create and set SMA line.
#             line = self.chart.create_line('SMA 50')
#             sma_data = self.calculate_sma(df, period=50)
#             line.set(sma_data)
#             # Update the chart.
#             self.chart.get_webview().update()

# def main():
#     api_key = ""  # Replace with your actual API key
#     app = QApplication(sys.argv)
#     window = StockChartWidget(api_key)
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()