# File: views/portfolio_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Signal

class PortfolioPage(QWidget):
    add_stock_signal = Signal(str, str, int, float)
    remove_stock_signal = Signal(str)
    refresh_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Table for displaying stock portfolio
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Symbol", "Company", "Quantity", "Avg Buy Price", "Current Price", "Market Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Buttons for adding/removing stocks and refreshing
        self.refresh_btn = QPushButton("Refresh Prices")
        self.add_btn = QPushButton("Add Stock")
        self.remove_btn = QPushButton("Remove Stock")

        # Button signals
        self.refresh_btn.clicked.connect(self.refresh_signal.emit)

        layout.addWidget(self.table)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.remove_btn)
        self.setLayout(layout)

    def update_portfolio(self, stocks):
        """Updates table with portfolio data."""
        self.table.setRowCount(len(stocks))
        for row, stock in enumerate(stocks):
            self.table.setItem(row, 0, QTableWidgetItem(stock["symbol"]))
            self.table.setItem(row, 1, QTableWidgetItem(stock["company"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(stock["quantity"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"${stock['avg_price']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"${stock['current_price']:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"${stock['market_value']:.2f}"))

