
import sys
sys.path.append('..')

from Client.views.components.styled_widgets import (
    PageTitleLabel, StyledTable, ScrollableContainer,
    StyledLineEdit, StyledLabel, StyledDateEdit,
    PrimaryButton, Card, SectionTitleLabel, create_form_field, RoundedCard
)
from PySide6.QtCore import Qt, QDateTime, Signal, QDate
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QTableWidgetItem, QSizePolicy, QScrollArea
from PySide6.QtGui import QFont


class HistoryView(QWidget):
    """
    View for transaction history page.

    Displays transaction data and provides UI for filtering.
    """
    # Define signals for user interactions
    filter_applied = Signal(str, str, str, str)  # from_date, to_date, type, search

    def __init__(self, parent=None):
        """Initialize the transaction history view."""
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the page layout and components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Page title
        title = PageTitleLabel("Transaction History")
        main_layout.addWidget(title)

        # Filters section
        self.filter_section = RoundedCard(parent=None, border_radius=16, shadow_enabled=True)
        filter_layout = QVBoxLayout(self.filter_section)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        filter_layout.setSpacing(10)

        filter_title = SectionTitleLabel("Filter Transactions", parent=self.filter_section)

        filter_form = QHBoxLayout()
        filter_form.setSpacing(10)

        symbol_input = StyledLineEdit(placeholder="Enter symbol", parent=self.filter_section)
        self.symbol_input = symbol_input
        symbol_layout = create_form_field("Symbol", symbol_input)

        # Start Date input
        start_date = StyledDateEdit(default_date=QDate(2024, 1, 1), parent=self.filter_section)
        self.start_date = start_date
        start_date_layout = create_form_field("Start Date", start_date)

        # End Date input
        end_date = StyledDateEdit(default_date=QDate(2024, 12, 30), parent=self.filter_section)
        self.end_date = end_date
        end_date_layout = create_form_field("End Date", end_date)

        filter_form.addLayout(symbol_layout, 2)
        filter_form.addLayout(start_date_layout, 2)
        filter_form.addLayout(end_date_layout, 2)

        # Button layout – Apply Filters
        button_layout = QHBoxLayout()
        self.apply_button = PrimaryButton("Apply Filters", object_name="applyFiltersButton", parent=self.filter_section)
        button_layout.addWidget(self.apply_button)
        button_layout.addStretch(1)

        # Add title, form and button layouts to the card layout
        filter_layout.addWidget(filter_title)
        filter_layout.addLayout(filter_form)
        filter_layout.addLayout(button_layout)

        main_layout.addWidget(self.filter_section)
        # Transactions table
        self.transactions_table = StyledTable()
        self.transactions_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.transactions_table.setColumnCount(6)  # Date, Symbol, Type, Quantity, Price, Total
        self.transactions_table.setHorizontalHeaderLabels(
            ["Date", "Symbol", "Type", "Quantity", "Price", "Total"])

        # Set column widths
        self.transactions_table.setColumnWidth(0, 100)  # Date
        self.transactions_table.setColumnWidth(1, 100)  # Symbol
        self.transactions_table.setColumnWidth(2, 50)  # Type
        self.transactions_table.setColumnWidth(3, 80)  # Quantity
        self.transactions_table.setColumnWidth(4, 80)  # Price
        self.transactions_table.setColumnWidth(5, 100)  # Total

        table_container = ScrollableContainer(self)
        table_container.layout.addWidget(self.transactions_table)

        main_layout.addWidget(table_container)

        # Connect signals
        self.apply_button.clicked.connect(self._on_apply_filters)

    def _on_apply_filters(self):
        """Handle filter application"""
        from_date = self.start_date.date().toString("yyyy-MM-dd")
        to_date = self.end_date.date().toString("yyyy-MM-dd")
        type_filter = self.type_combo.currentText()
        search_text = self.search_input.text()

        self.filter_applied.emit(from_date, to_date, type_filter, search_text)

    def display_transactions(self, transactions):
        """
        Display transactions in the table.

        Args:
            transactions: List of transaction dictionaries
        """
        print("history view data:", transactions)

        self.transactions_table.setRowCount(0)  # Clear table

        for i, tx in enumerate(transactions):
            self.transactions_table.insertRow(i)

            date_str = tx["date"]
            if "T" in date_str:
                parts = date_str.split("T")
                date_part = parts[0]
                # time_part = parts[1].split(".")[0] if "." in parts[1] else parts[1]
                # tx_date_str = f"{date_part} {time_part}"
                tx_date_str = date_part
            else:
                tx_date_str = date_str

            self.transactions_table.setItem(i, 0, CustomTableItem(tx_date_str))

            # Symbol in bold
            self.transactions_table.setItem(i, 1, CustomTableItem(tx["symbol"]))
            self.transactions_table.item(i, 1).setFont(QFont("Arial", 10, QFont.Bold))

            # Create custom widget for transaction type (with color)
            type_widget = QWidget()
            type_layout = QHBoxLayout(type_widget)
            type_layout.setContentsMargins(5, 2, 5, 2)

            type_label = QLabel("Buy" if tx["type"] == 0 else "Sell")
            type_label.setAlignment(Qt.AlignCenter)
            type_label.setStyleSheet(f"""
                background-color: {'#DCFCE7' if tx["type"] == 0 else '#FEE2E2'};
                color: {'#166534' if tx["type"] == 0 else '#991B1B'};
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
            """)
            type_layout.addWidget(type_label)

            self.transactions_table.setCellWidget(i, 2, type_widget)
            self.transactions_table.setItem(i, 3, CustomTableItem(str(tx["quantity"])))
            self.transactions_table.setItem(i, 4, CustomTableItem(f"${tx['price']:.2f}"))
            self.transactions_table.setItem(i, 5, CustomTableItem(f"${(tx['quantity'] * tx['price']):.2f}"))

            print("history view", tx)

        # self.transactions_table.resizeColumnsToContents()

    def show_error(self, message):
        """Display error message to user."""
        # You could implement a proper error dialog here
        print(f"Error: {message}")


class CustomTableItem(QTableWidgetItem):
    """Custom QTableWidgetItem with text alignment"""

    def __init__(self, text):
        super().__init__(text)
        self.setTextAlignment(Qt.AlignCenter)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    view = HistoryView()
    view.show()

    # For testing, call display_transactions with sample data
    sample_transactions = [
        {'symbol': 'AAPL', 'date': '2025-03-13T14:16:00.71644', 'type': 0, 'quantity': 10, 'price': 100.0},
        {'symbol': 'GOOGL', 'date': '2025-03-13T14:16:00.7210188', 'type': 0, 'quantity': 5, 'price': 200.0},
        {'symbol': 'TSLA', 'date': '2025-03-13T14:16:00.7210245', 'type': 1, 'quantity': 20, 'price': 300.0}
    ]
    view.display_transactions(sample_transactions)

    sys.exit(app.exec_())
