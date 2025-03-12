from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QDateEdit
from PySide6.QtCore import Qt, QDate
from Widgets.StockChartWidget import StockChartWidget  # Import the stock chart widget
from Presenters.mainPresenters.stockPresenter import StockPresenter  # Import the presenter

class StockSearchPage(QWidget):
    def __init__(self, parent=None):
        """
        Stock Search Page UI for searching stock data.

        :param presenter: The presenter that handles the logic.
        :param parent: Parent widget.
        """
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
        self.search_btn.clicked.connect(self.search_stock)  # Connect button to search_stock()

        input_layout.addWidget(self.ticker_input)
        input_layout.addWidget(QLabel("Start:"))
        input_layout.addWidget(self.start_date_input)
        input_layout.addWidget(QLabel("End:"))
        input_layout.addWidget(self.end_date_input)
        input_layout.addWidget(self.search_btn)

        # Stock Chart Widget
        self.stock_chart = StockChartWidget()  # Create the stock chart widget

        layout.addLayout(input_layout)
        layout.addWidget(self.stock_chart)  # Add stock chart widget

        self.setLayout(layout)

    def search_stock(self):
        """Handles stock search when the user clicks the Search button."""
        ticker = self.ticker_input.text().strip().upper()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")

        if not ticker:
            self.display_error("Stock symbol cannot be empty!")
            return

        # Send the request to the presenter to fetch stock data
        self.presenter.fetch_stock_data(ticker, start_date, end_date)

    def update_chart(self,ticker, start_date, end_date, stock_data):
        """Updates the stock chart widget with new data."""
        self.stock_chart.update_chart(ticker, start_date, end_date, stock_data)  # Assuming `display_chart()` is a method in StockChartWidget

    def display_error(self, message):
        """Displays an error message to the user (could be improved with a UI label)."""
        print(f"❌ Error: {message}")  # Replace with a proper UI error message
