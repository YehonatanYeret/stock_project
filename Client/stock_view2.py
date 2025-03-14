from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QGroupBox, QHBoxLayout, QSpinBox, QRadioButton
)
from PySide6.QtCore import Qt, QDate
from StockChartWidget import StockChartWidget

from stock_presenter2 import StockPresenter


class StockView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Market Dashboard")
        self.setMinimumSize(1000, 600)
        self.init_ui()

        # COnnect to the presenter
        self.presenter = StockPresenter(self)
        self.presenter.stock_data_received.connect(self.update_stock_info)
        self.presenter.order_processed.connect(self.show_order_confirmation)

    def load_styles(self):
        """Loads QSS stylesheet."""
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        layout = QGridLayout()

        # Search Bar
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter Stock Symbol")
        self.search_button = QPushButton("Search")
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate(2024, 1, 1))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate(2024, 1, 31))

        layout.addWidget(QLabel("Stock Symbol"), 0, 0)
        layout.addWidget(self.symbol_input, 0, 1)
        layout.addWidget(QLabel("Start Date"), 0, 2)
        layout.addWidget(self.start_date, 0, 3)
        layout.addWidget(QLabel("End Date"), 0, 4)
        layout.addWidget(self.end_date, 0, 5)
        layout.addWidget(self.search_button, 0, 6)

        # Stock Info
        self.stock_info = QLabel("Stock Info Placeholder")
        self.chart_widget = StockChartWidget()

        layout.addWidget(self.stock_info, 1, 0, 1, 4)
        layout.addWidget(self.chart_widget, 2, 0, 1, 6)

        # Order Section
        order_box = QGroupBox("Place Order")
        order_layout = QVBoxLayout()

        self.buy_button = QRadioButton("Buy")
        self.sell_button = QRadioButton("Sell")
        self.buy_button.setChecked(True)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)

        self.place_order_button = QPushButton("Place Order")

        order_layout.addWidget(self.buy_button)
        order_layout.addWidget(self.sell_button)
        order_layout.addWidget(QLabel("Quantity"))
        order_layout.addWidget(self.quantity_input)
        order_layout.addWidget(self.place_order_button)
        order_box.setLayout(order_layout)

        layout.addWidget(order_box, 1, 4, 1, 2)

        self.setLayout(layout)

        self.load_styles()

    def update_stock_info(self, stock_data):
        """Update the stock information display."""
        self.stock_info.setText(f"{stock_data['name']} ({stock_data['ticker']}) - ${stock_data['aggregateData']}")

    def show_order_confirmation(self, message):
        """Display order confirmation message."""
        self.stock_info.setText(message)
