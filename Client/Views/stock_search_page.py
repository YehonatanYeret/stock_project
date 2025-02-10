from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QDateEdit
from PySide6.QtCore import Qt, QDate
from Widgets.StockChartWidget import StockChartWidget  # Import StockChartWidget

class StockSearchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Input Section
        input_layout = QHBoxLayout()

        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Enter Stock Symbol (e.g., AAPL)")

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate().addMonths(-1))  # Default to 1 month ago

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())  # Default to today

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_stock)  # Connect button

        input_layout.addWidget(self.ticker_input)
        input_layout.addWidget(QLabel("Start:"))
        input_layout.addWidget(self.start_date_input)
        input_layout.addWidget(QLabel("End:"))
        input_layout.addWidget(self.end_date_input)
        input_layout.addWidget(self.search_btn)

        # Stock Chart Widget
        self.stock_chart = StockChartWidget()  # Pass API key

        layout.addLayout(input_layout)
        layout.addWidget(self.stock_chart)  # Add stock chart widget

        self.setLayout(layout)

    def search_stock(self):
        """Fetch stock data and update chart."""
        ticker = self.ticker_input.text().strip().upper()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        if not ticker:
            return  # Do nothing if ticker is empty

        self.stock_chart.fetch_and_display_chart(ticker, start_date, end_date)  # Update chart
