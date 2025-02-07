from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QTableWidget, QTableWidgetItem, QLabel, QPushButton
)
from PySide6.QtCore import Qt, Slot

# PortfolioView.py
class PortfolioWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Portfolio")
        self.setFixedSize(800, 600)  # Adjusted size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QWidget#container {
                background-color: white;
                border-radius: 8px;
            }
            QLabel#title {
                color: #1a73e8;
                font-size: 28px;
                font-weight: bold;
            }
            QLabel {
                color: #333333;
                font-size: 16px;
                margin-bottom: 8px;
            }
            QTableWidget {
                border: 1px solid #dddddd;
                border-radius: 6px;
                font-size: 16px;
                color: #333333;
                background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 18px;
                margin-top: 15px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)

        # Create main container widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("container")
        self.setCentralWidget(self.central_widget)

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        self.central_widget.setLayout(layout)

        # Title
        self.label_title = QLabel("Portfolio Overview")
        self.label_title.setObjectName("title")
        self.label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_title)

        # User ID display
        self.label_user_id = QLabel("User ID: Not Provided")
        self.label_user_id.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_user_id)

        # Portfolio table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Stock", "Quantity", "Value"])
        self.table.setRowCount(0)  # Start with an empty table
        layout.addWidget(self.table)

        # Refresh button
        self.btn_refresh = QPushButton("Refresh Portfolio")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_portfolio)
        layout.addWidget(self.btn_refresh)

        # Message label
        self.label_message = QLabel()
        self.label_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_message)

        # Center the window
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

    @Slot()
    def refresh_portfolio(self):
        # Call presenter to fetch portfolio data
        self.presenter.fetch_portfolio()

    def update_table(self, portfolio_data):
        """
        Update the table with new portfolio data.
        :param portfolio_data: List of dictionaries containing stock data.
        """
        self.table.setRowCount(len(portfolio_data))
        for row, stock in enumerate(portfolio_data):
            self.table.setItem(row, 0, QTableWidgetItem(stock["stock"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(stock["quantity"])))
            self.table.setItem(row, 2, QTableWidgetItem(f"${stock['value']:.2f}"))

    def show_message(self, message):
        """
        Display a message to the user.
        :param message: Message string.
        """
        self.label_message.setText(message)

    def update_user_id(self, user_id):
        """
        Update the user ID label in the PortfolioWindow.
        :param user_id: The user ID to display.
        """
        self.label_user_id.setText(f"User ID: {user_id}")
