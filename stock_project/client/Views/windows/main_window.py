\from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QPushButton)
from PySide6.QtCore import Qt
from ..widgets.portfolio_widget import PortfolioWidget
from ..widgets.history_widget import HistoryWidget
from ..widgets.advisor_widget import AdvisorWidget
from ..dialogs.buy_dialog import BuyDialog
from ..dialogs.sell_dialog import SellDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ניהול תיק מניות")
        self.setMinimumSize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        # Central widget with horizontal layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left side - History
        self.history_widget = HistoryWidget()
        main_layout.addWidget(self.history_widget)

        # Center - Portfolio and Trading buttons
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)

        # Trading buttons
        buttons_layout = QHBoxLayout()
        self.buy_button = QPushButton("קנייה")
        self.sell_button = QPushButton("מכירה")
        self.buy_button.clicked.connect(self.show_buy_dialog)
        self.sell_button.clicked.connect(self.show_sell_dialog)
        buttons_layout.addWidget(self.buy_button)
        buttons_layout.addWidget(self.sell_button)
        center_layout.addLayout(buttons_layout)

        # Portfolio
        self.portfolio_widget = PortfolioWidget()
        center_layout.addWidget(self.portfolio_widget)
        main_layout.addWidget(center_widget, stretch=2)

        # Right side - AI Advisor
        self.advisor_widget = AdvisorWidget()
        main_layout.addWidget(self.advisor_widget)

    def show_buy_dialog(self):
        dialog = BuyDialog(self)
        dialog.exec()

    def show_sell_dialog(self):
        dialog = SellDialog(self)
        dialog.exec()