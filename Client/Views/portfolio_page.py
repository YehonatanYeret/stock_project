from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from lightweight_charts.widgets import QtChart
from PySide6.QtCore import Signal
import pandas as pd



class PortfolioPage(QWidget):
    # Signal for adding a stock (can be connected to presenter logic)
    add_stock_signal = Signal(str, str, int, float)
    remove_stock_signal = Signal(str)
    refresh_signal = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the portfolio page UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        # --- USER PROFILE SECTION ---
        profile_layout = QHBoxLayout()
        
        self.user_icon = QLabel()
        pixmap = QPixmap("user_icon.png")  # Dummy icon
        self.user_icon.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
        
        self.username_label = QLabel("Username: JohnDoe")  # Dummy name
        self.username_label.setStyleSheet("color: white; font-size: 18px;")
        
        profile_layout.addWidget(self.user_icon)
        profile_layout.addWidget(self.username_label)
        layout.addLayout(profile_layout)
        
        # --- STOCK CHART SECTION ---
        self.chart = QtChart(self)
        self.chart.get_webview().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart.get_webview().setMinimumSize(800, 400)
        layout.addWidget(self.chart.get_webview(), stretch=1)
        
        # --- LOGS BUTTON ---
        self.log_button = QPushButton("Show Logs")
        self.log_button.setStyleSheet("background-color: #4a4d4f; color: white; padding: 10px;")
        self.log_button.clicked.connect(self.fetch_logs)
        layout.addWidget(self.log_button)
        
        self.setLayout(layout)
        self.load_dummy_chart()
    
    def fetch_logs(self):
        """Fetch logs from the server"""
        print("Fetching logs...")
        # TODO: Replace with real API request
        # response = requests.get("http://server.com/api/logs")
        # logs = response.json()
        print("Dummy logs: [Trade Executed, Market Closed]")
    
    def load_dummy_chart(self):
        """Load dummy stock data into the chart"""
        dummy_data = [
            {'t': 1707600000000, 'o': 100, 'h': 110, 'l': 99, 'c': 105, 'v': 5000},
            {'t': 1707686400000, 'o': 105, 'h': 115, 'l': 104, 'c': 112, 'v': 6000},
            {'t': 1707774800000, 'o': 112, 'h': 118, 'l': 110, 'c': 116, 'v': 7000},
            {'t': 1707776800000, 'o': 113, 'h': 110, 'l': 110, 'c': 115, 'v': 8000},
            {'t': 1707778800000, 'o': 111, 'h': 115, 'l': 166, 'c': 112, 'v': 9000},
            {'t': 1707782800000, 'o': 108, 'h': 111, 'l': 75, 'c': 146, 'v': 10000},
            {'t': 1707782800000, 'o': 92, 'h': 98, 'l': 34, 'c': 115, 'v': 11000},
            {'t': 1707787000000, 'o': 12, 'h': 118, 'l': 150, 'c': 116, 'v': 12000},
            {'t': 1709779800000, 'o': 112, 'h': 118, 'l': 120, 'c': 116, 'v': 13000}
        ]
        df = pd.DataFrame(dummy_data)
        df['date'] = pd.to_datetime(df['t'], unit='ms')
        df = df.rename(columns={'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
        self.chart.set(df[['date', 'open', 'high', 'low', 'close', 'volume']])
        
        # Compute SMA and add to chart
        sma = df['close'].rolling(window=2).mean()
        sma_df = pd.DataFrame({'time': df['date'], 'SMA 2': sma}).dropna()
        line = self.chart.create_line('SMA 2')
        line.set(sma_df)
        self.chart.get_webview().update()
        print(" Dummy chart loaded")
        print(df[['date', 'open', 'high', 'low', 'close', 'volume']])



    def update_portfolio(self, portfolio_data):
        """Update portfolio summary and holdings table."""
        self.portfolio_value.setText(f"Portfolio Value: ${portfolio_data['value']}")
        self.daily_change.setText(f"Daily Change: {portfolio_data['change']}")
        # Update holdings table
        self.table.setRowCount(len(portfolio_data['holdings']))
        for row, (stock, shares, price) in enumerate(portfolio_data['holdings']):
            self.table.setItem(row, 0, QTableWidgetItem(stock))
            self.table.setItem(row, 1, QTableWidgetItem(str(shares)))
            self.table.setItem(row, 2, QTableWidgetItem(f"${price:.2f}"))

