# File: views/stock_search_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt

class StockSearchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Search Section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Stock Symbol")
        self.search_btn = QPushButton("Search")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        
        # Stock Info Display
        self.stock_symbol_label = QLabel("Symbol: -")
        self.stock_name_label = QLabel("Name: -")
        self.stock_price_label = QLabel("Price: -")
        self.stock_change_label = QLabel("Change: -")
        
        # Style labels
        for label in [self.stock_symbol_label, self.stock_name_label, 
                      self.stock_price_label, self.stock_change_label]:
            label.setStyleSheet("""
                font-size: 16px;
                color: #4CAF50;
                padding: 5px;
            """)
            label.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.stock_symbol_label)
        layout.addWidget(self.stock_name_label)
        layout.addWidget(self.stock_price_label)
        layout.addWidget(self.stock_change_label)
        layout.addStretch(1)

    def update_stock_info(self, stock_data):
        """Update UI with retrieved stock information"""
        self.stock_symbol_label.setText(f"Symbol: {stock_data.get('symbol', '-')}")
        self.stock_name_label.setText(f"Name: {stock_data.get('name', '-')}")
        self.stock_price_label.setText(f"Price: ${stock_data.get('price', '-'):.2f}")
        self.stock_change_label.setText(f"Change: {stock_data.get('change', '-'):.2f}%")