import sys

sys.path.append('..')
from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QTableWidgetItem

from Client.views.components.styled_widgets import (
    PageTitleLabel, StyledTable, ScrollableContainer,
    StyledLineEdit, StyledLabel, StyledDateEdit,
    PrimaryButton, Card
)


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
        filter_card = Card(self)
        filter_layout = QVBoxLayout(filter_card)

        # Date range filters
        date_filter_layout = QHBoxLayout()
        date_filter_layout.setSpacing(10)

        from_date_label = StyledLabel("From:", color="#334155")
        self.from_date_edit = StyledDateEdit()
        self.from_date_edit.setDate(QDateTime.currentDateTime().addMonths(-1).date())

        to_date_label = StyledLabel("To:", color="#334155")
        self.to_date_edit = StyledDateEdit()
        self.to_date_edit.setDate(QDateTime.currentDateTime().date())

        date_filter_layout.addWidget(from_date_label)
        date_filter_layout.addWidget(self.from_date_edit)
        date_filter_layout.addWidget(to_date_label)
        date_filter_layout.addWidget(self.to_date_edit)
        date_filter_layout.addStretch()

        # Transaction type filter
        type_filter_layout = QHBoxLayout()
        type_filter_layout.setSpacing(10)

        type_label = StyledLabel("Type:", color="#334155")
        self.type_combo = QComboBox()
        self.type_combo.setFixedHeight(38)
        self.type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
        """)
        self.type_combo.addItem("All")
        self.type_combo.addItem("Buy")
        self.type_combo.addItem("Sell")

        search_label = StyledLabel("Search:", color="#334155")
        self.search_input = StyledLineEdit(placeholder="Symbol")

        type_filter_layout.addWidget(type_label)
        type_filter_layout.addWidget(self.type_combo)
        type_filter_layout.addWidget(search_label)
        type_filter_layout.addWidget(self.search_input)

        # Apply filters button
        self.apply_button = PrimaryButton("Apply Filters")
        apply_button_layout = QHBoxLayout()
        apply_button_layout.addStretch()
        apply_button_layout.addWidget(self.apply_button)

        # Add all filter layouts
        filter_layout.addLayout(date_filter_layout)
        filter_layout.addLayout(type_filter_layout)
        filter_layout.addLayout(apply_button_layout)

        main_layout.addWidget(filter_card)

        # Transactions table
        self.transactions_table = StyledTable()
        self.transactions_table.setColumnCount(6)  # Date, Symbol Type, Quantity, Price, Total
        self.transactions_table.setHorizontalHeaderLabels(
            ["Date", "Symbol", "Type", "Quantity", "Price", "Total"])

        # Set column widths
        self.transactions_table.setColumnWidth(0, 150)  # Date
        self.transactions_table.setColumnWidth(1, 80)  # Symbol
        self.transactions_table.setColumnWidth(2, 50)  # Type
        self.transactions_table.setColumnWidth(3, 80)  # Quantity
        self.transactions_table.setColumnWidth(4, 80)  # Price
        self.transactions_table.setColumnWidth(5, 100)  # Total

        # Create a scrollable container for the table
        table_container = ScrollableContainer()
        table_container_layout = QVBoxLayout(table_container.widget())
        table_container_layout.addWidget(self.transactions_table)

        main_layout.addWidget(table_container)

        # Connect signals
        self.apply_button.clicked.connect(self._on_apply_filters)

    def _on_apply_filters(self):
        """Handle filter application"""
        from_date = self.from_date_edit.date().toString("yyyy-MM-dd")
        to_date = self.to_date_edit.date().toString("yyyy-MM-dd")
        type_filter = self.type_combo.currentText()
        search_text = self.search_input.text()

        self.filter_applied.emit(from_date, to_date, type_filter, search_text)

    def display_transactions(self, transactions):
        """
        Display transactions in the table.

        Args:
            transactions: List of transaction dictionaries
        """

        self.transactions_table.setRowCount(0)  # Clear table

        for i, tx in enumerate(transactions):
            self.transactions_table.insertRow(i)

            # Format transaction date
            date_str = tx["date"]
            tx_date = QDateTime.fromString(date_str, "yyyy-MM-ddTHH:mm:ss.zzz").toString("yyyy-MM-dd HH:mm:ss")

            # Set cell values
            self.transactions_table.setItem(i, 0, CustomTableItem(tx_date))
            self.transactions_table.setItem(i, 1, CustomTableItem(tx["symbol"]))

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
            self.transactions_table.setItem(i, 5, CustomTableItem(f"${(tx["quantity"] * tx['price']):.2f}"))

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
    sys.exit(app.exec_())
