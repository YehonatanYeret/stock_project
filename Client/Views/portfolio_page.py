# File: views/portfolio_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                               QTableWidgetItem, QHeaderView)

class PortfolioPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.portfolio_table = QTableWidget()
        self.portfolio_table.setColumnCount(4)
        self.portfolio_table.setHorizontalHeaderLabels(
            ["Symbol", "Name", "Quantity", "Total Value"]
        )
        self.portfolio_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.portfolio_table.setStyleSheet("""
            QTableWidget {
                background-color: #3c3f41;
                color: white;
                selection-background-color: #4a4d4f;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: white;
                padding: 5px;
                border: 1px solid #555;
            }
        """)
        
        layout.addWidget(self.portfolio_table)

    def update_portfolio(self, portfolio_data):
        """Update portfolio table with current holdings"""
        self.portfolio_table.setRowCount(0)
        
        for stock in portfolio_data:
            row_position = self.portfolio_table.rowCount()
            self.portfolio_table.insertRow(row_position)
            
            self.portfolio_table.setItem(
                row_position, 0, QTableWidgetItem(stock.get('symbol', 'N/A'))
            )
            self.portfolio_table.setItem(
                row_position, 1, QTableWidgetItem(stock.get('name', 'N/A'))
            )
            self.portfolio_table.setItem(
                row_position, 2, QTableWidgetItem(str(stock.get('quantity', 0)))
            )
            self.portfolio_table.setItem(
                row_position, 3, QTableWidgetItem(f"${stock.get('total_value', 0):.2f}")
            )