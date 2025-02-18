"""
portfolio_page.py - Portfolio Page Implementation for Stock Management System

This module implements the Portfolio page view component following the MVP pattern.
It provides a modern, interactive interface for users to view their stock portfolio,
including performance charts, holdings information, and trade history.

Key Features:
- Interactive performance chart with time range selection
- Toggle-able table view switching between holdings and trade history
- Modern blue-themed UI with consistent styling
- Responsive layout that adjusts to window size

Dependencies:
- PySide6: Qt framework for the UI components
- Qt Charts: For rendering portfolio performance charts

Author: [Your Name]
Date: February 2025
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QStackedWidget, QStyle
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtGui import QPainter, QFont, QPalette, QColor

# Style constants for consistent theming
STYLE_CONSTANTS = {
    'COLORS': {
        'background': '#f8fafc',
        'primary': '#3b82f6',
        'primary_hover': '#2563eb',
        'primary_pressed': '#1d4ed8',
        'text': '#1e293b',
        'text_light': '#64748b',
        'border': '#e2e8f0',
        'success': '#10b981',
        'danger': '#ef4444'
    },
    'FONTS': {
        'header': QFont('Segoe UI', 12, QFont.Bold),
        'body': QFont('Segoe UI', 10),
        'small': QFont('Segoe UI', 9)
    }
}

# Main stylesheet for the portfolio page
PORTFOLIO_STYLE = """
    QWidget {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Segoe UI';
    }
    
    QPushButton {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        min-width: 80px;
    }
    
    QPushButton:hover {
        background-color: #2563eb;
    }
    
    QPushButton:pressed {
        background-color: #1d4ed8;
    }
    
    QPushButton:checked {
        background-color: #1d4ed8;
    }
    
    QTableWidget {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
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
    
    QLabel#portfolioValue {
        font-size: 24px;
        font-weight: bold;
        color: #1e293b;
    }
    
    QLabel#dailyPL {
        font-size: 16px;
        font-weight: bold;
    }
    
    QFrame#chartFrame {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
    }
"""

class PortfolioPage(QWidget):
    """
    Main portfolio page widget that displays user's portfolio information.
    
    Signals:
        refresh_requested: Emitted when user requests data refresh
        stock_selected: Emitted when user selects a stock from the holdings table
    """

    refresh_requested = Signal()
    stock_selected = Signal(str)

    def __init__(self, parent=None):
        """Initialize the portfolio page."""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup the main user interface components."""
        self.setStyleSheet(PORTFOLIO_STYLE)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add UI sections
        main_layout.addLayout(self.setup_header())
        main_layout.addWidget(self.setup_chart_section(), 2)
        main_layout.addWidget(self.setup_table_section(), 1)

    def setup_header(self):
        """
        Setup the header section with user info and portfolio summary.
        Returns:
            QHBoxLayout: The header layout
        """
        header_layout = QHBoxLayout()

        # User information
        user_section = QVBoxLayout()
        user_name = QLabel("John Doe")
        user_name.setFont(STYLE_CONSTANTS['FONTS']['header'])
        user_section.addWidget(user_name)

        # Portfolio value and daily change
        self.portfolio_value = QLabel("$0.00")
        self.portfolio_value.setObjectName("portfolioValue")

        self.daily_pl = QLabel("+$0.00 (0.00%)")
        self.daily_pl.setObjectName("dailyPL")

        value_section = QVBoxLayout()
        value_section.addWidget(self.portfolio_value)
        value_section.addWidget(self.daily_pl)

        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        refresh_btn.clicked.connect(self.refresh_requested.emit)

        header_layout.addLayout(user_section)
        header_layout.addStretch()
        header_layout.addLayout(value_section)
        header_layout.addWidget(refresh_btn)

        return header_layout

    def setup_chart_section(self):
        """
        Setup the chart section with performance chart and time range controls.
        Returns:
            QFrame: The chart container frame
        """
        chart_frame = QFrame()
        chart_frame.setObjectName("chartFrame")
        chart_layout = QVBoxLayout(chart_frame)

        # Time range controls
        controls_layout = QHBoxLayout()
        self.time_range_buttons = []

        for range_text in ["1D", "1W", "1M", "3M", "1Y", "ALL"]:
            btn = QPushButton(range_text)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            self.time_range_buttons.append(btn)
            controls_layout.addWidget(btn)

        controls_layout.addStretch()

        # Chart view
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)
        self.chart_view.setMinimumHeight(400)

        # Initialize empty chart
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)
        chart.legend().hide()
        self.chart_view.setChart(chart)

        chart_layout.addLayout(controls_layout)
        chart_layout.addWidget(self.chart_view)

        return chart_frame

    def setup_table_section(self):
        """
        Setup the table section with toggle-able views for holdings and trade history.
        Returns:
            QFrame: The table container frame
        """
        table_frame = QFrame()
        layout = QVBoxLayout(table_frame)

        # View toggle controls
        toggle_layout = QHBoxLayout()
        self.view_toggle = QPushButton("Switch to Trade History")
        self.view_toggle.setCheckable(True)
        toggle_layout.addWidget(self.view_toggle)
        toggle_layout.addStretch()

        # Main table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        layout.addLayout(toggle_layout)
        layout.addWidget(self.table)

        return table_frame

    def update_portfolio_value(self, value: float, daily_change: float, daily_change_pct: float):
        """
        Update the portfolio value and daily change displays.
        
        Args:
            value: Current portfolio value
            daily_change: Daily change in absolute terms
            daily_change_pct: Daily change as a percentage
        """
        self.portfolio_value.setText(f"${value:,.2f}")

        change_color = (STYLE_CONSTANTS['COLORS']['success']
                        if daily_change >= 0
                        else STYLE_CONSTANTS['COLORS']['danger'])
        sign = "+" if daily_change >= 0 else ""

        self.daily_pl.setText(
            f"{sign}${daily_change:,.2f} ({sign}{daily_change_pct:.2f}%)"
        )
        self.daily_pl.setStyleSheet(f"color: {change_color}")

    def set_holdings_view(self):
        """Configure table for displaying holdings data."""
        headers = ["Symbol", "Quantity", "Buy Price", "Current Price",
                   "Daily Change (%)", "Profit/Loss"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def set_trade_history_view(self):
        """Configure table for displaying trade history data."""
        headers = ["Date", "Symbol", "Type", "Quantity", "Price", "Fees"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def update_chart_data(self, series: QLineSeries):
        """
        Update the performance chart with new data.
        
        Args:
            series: QLineSeries containing the chart data points
        """
        chart = self.chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(series)

        # Update axes
        axis_x = QDateTimeAxis()
        axis_x.setFormat("MMM dd")
        axis_y = QValueAxis()
        axis_y.setLabelFormat("$%.2f")

        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def resizeEvent(self, event):
        """Handle widget resize events to maintain responsive layout."""
        super().resizeEvent(event)
        # Adjust chart size based on new widget size
        if hasattr(self, 'chart_view'):
            min_height = min(400, self.height() * 0.4)
            self.chart_view.setMinimumHeight(int(min_height))

"""
Usage Example:

from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
portfolio_page = PortfolioPage()
portfolio_page.show()
sys.exit(app.exec())
"""