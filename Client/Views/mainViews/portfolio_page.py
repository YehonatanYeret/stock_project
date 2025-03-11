# File: views/portfolio_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QHeaderView, QFrame, QStyle
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtGui import QPainter, QFont

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
# File: views/portfolio_page.py
class PortfolioPage(QWidget):
    refresh_requested = Signal()
    stock_selected = Signal(str)
    chart_range_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.presenter = None
        self.table = QTableWidget()
        self.view_toggle = QPushButton("Switch to Trade History")
        self.time_range_buttons = []
        self.portfolio_value = QLabel("$0.00")
        self.daily_pl = QLabel("+$0.00 (0.00%)")
        self.chart_view = QChartView()  # Initialize chart_view

    def set_presenter(self, presenter):
        self.presenter = presenter
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(PORTFOLIO_STYLE)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(self.setup_header())
        main_layout.addWidget(self.setup_chart_section(), 2)
        main_layout.addWidget(self.setup_table_section(), 1)

    def setup_header(self):
        header_layout = QHBoxLayout()
        user_section = QVBoxLayout()
        user_id = QLabel(f"User ID: {self.presenter.get_user_id()}")
        user_id.setFont(STYLE_CONSTANTS['FONTS']['header'])
        user_section.addWidget(user_id)
        self.portfolio_value.setObjectName("portfolioValue")
        self.daily_pl.setObjectName("dailyPL")
        value_section = QVBoxLayout()
        value_section.addWidget(self.portfolio_value)
        value_section.addWidget(self.daily_pl)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        refresh_btn.clicked.connect(self.refresh_requested.emit)
        header_layout.addLayout(user_section)
        header_layout.addStretch()
        header_layout.addLayout(value_section)
        header_layout.addWidget(refresh_btn)
        return header_layout

    def setup_chart_section(self):
        chart_frame = QFrame()
        chart_frame.setObjectName("chartFrame")
        chart_layout = QVBoxLayout(chart_frame)
        controls_layout = QHBoxLayout()
        self.time_range_buttons = []
        for range_text in ["1D", "1W", "1M", "3M", "1Y", "ALL"]:
            btn = QPushButton(range_text)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda checked, r=range_text: self.chart_range_changed.emit(r))
            self.time_range_buttons.append(btn)
            controls_layout.addWidget(btn)
        controls_layout.addStretch()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRubberBand(QChartView.RectangleRubberBand)
        self.chart_view.setMinimumHeight(400)
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)
        chart.legend().hide()
        self.chart_view.setChart(chart)
        chart_layout.addLayout(controls_layout)
        chart_layout.addWidget(self.chart_view)
        return chart_frame

    def setup_table_section(self):
        table_frame = QFrame()
        layout = QVBoxLayout(table_frame)
        toggle_layout = QHBoxLayout()
        toggle_layout.addWidget(self.view_toggle)
        toggle_layout.addStretch()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addLayout(toggle_layout)
        layout.addWidget(self.table)
        return table_frame

    def update_portfolio_value(self, value: float, daily_change: float, daily_change_pct: float):
        self.portfolio_value.setText(f"${value:,.2f}")
        change_color = (STYLE_CONSTANTS['COLORS']['success']
                        if daily_change >= 0
                        else STYLE_CONSTANTS['COLORS']['danger'])
        sign = "+" if daily_change >= 0 else ""
        self.daily_pl.setText(f"{sign}${daily_change:,.2f} ({sign}{daily_change_pct:.2f}%)")
        self.daily_pl.setStyleSheet(f"color: {change_color}")

    def set_holdings_view(self):
        headers = ["Symbol", "Quantity", "Buy Price", "Current Price", "Daily Change (%)", "Profit/Loss"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def set_trade_history_view(self):
        headers = ["Date", "Symbol", "Type", "Quantity", "Price", "Fees"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

    def update_chart_data(self, series: QLineSeries):
        chart = self.chart_view.chart()
        chart.removeAllSeries()
        chart.addSeries(series)
        axis_x = QDateTimeAxis()
        axis_x.setFormat("MMM dd")
        axis_y = QValueAxis()
        axis_y.setLabelFormat("$%.2f")
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'chart_view'):
            min_height = min(400, self.height() * 0.4)
            self.chart_view.setMinimumHeight(int(min_height))