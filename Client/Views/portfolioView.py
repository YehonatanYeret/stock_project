# File: views/portfolio_page.py
from PySide6.QtCharts import QChartView
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, \
    QHBoxLayout
from PySide6.QtCore import Signal

STYLE_CONSTANTS = {
    'COLORS': {
        'background': '#f8fafc',
        'primary': '#3b82f6',
        'primary_hover': '#2563eb',
        'primary_pressed': '#1d4ed8',
        'text': '#1e293b',
        'text_light': '#64748b',
        'border': '#e2e8f0',
    }
}

BLUE_THEME_STYLE = """
    QWidget {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    QPushButton {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #2563eb;
    }
    
    QPushButton:pressed {
        background-color: #1d4ed8;
    }
    
    QTableWidget {
        background-color: white;
        border: 1px solid #e2e8f0;
        gridline-color: #e2e8f0;
    }
    
    QHeaderView::section {
        background-color: #f1f5f9;
        color: #64748b;
        border: none;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        padding: 8px;
        font-weight: bold;
    }
    
    QComboBox {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 6px;
        color: #1e293b;
    }
    
    QComboBox:hover {
        border-color: #3b82f6;
    }
    
    QLabel#portfolioValue {
        font-size: 24px;
        font-weight: bold;
        color: #1e293b;
    }
    
    QLabel#dailyPL {
        font-size: 16px;
        font-weight: bold;
    }
"""


class PortfolioPage(QWidget):
    add_stock_signal = Signal(str, str, int, float)
    remove_stock_signal = Signal(str)
    refresh_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(BLUE_THEME_STYLE)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Updated Header Section
        header_layout = self.setup_header()

        # Enhanced Chart Section
        chart_section = self.setup_enhanced_chart()

        # Toggle-able Table Section
        table_section = self.setup_toggle_table()

        main_layout.addLayout(header_layout)
        main_layout.addWidget(chart_section, 2)  # Give chart more vertical space
        main_layout.addWidget(table_section, 1)

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

    def setup_enhanced_chart(self):
        container = QFrame()
        layout = QVBoxLayout(container)

        # Time Range Controls
        controls_layout = QHBoxLayout()
        self.time_range_buttons = []
        for range_text in ["1D", "1W", "1M", "1Y", "ALL"]:
            btn = QPushButton(range_text)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            self.time_range_buttons.append(btn)
            controls_layout.addWidget(btn)
        controls_layout.addStretch()

        # Enhanced Chart View
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)
        self.chart_view.setMinimumHeight(400)  # Make chart larger

        layout.addLayout(controls_layout)
        layout.addWidget(self.chart_view)

        return container

    def setup_toggle_table(self):
        container = QFrame()
        layout = QVBoxLayout(container)

        # View Toggle
        toggle_layout = QHBoxLayout()
        self.view_toggle = QPushButton("Switch to Trade History")
        toggle_layout.addWidget(self.view_toggle)
        toggle_layout.addStretch()

        # Combined Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)

        layout.addLayout(toggle_layout)
        layout.addWidget(self.table)

        return container
