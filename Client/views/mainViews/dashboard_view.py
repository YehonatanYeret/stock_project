import sys
import datetime

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QSizePolicy, QComboBox, QPushButton,
    QGraphicsDropShadowEffect, QHeaderView, QScrollArea
)
from PySide6.QtGui import (
    QPixmap, QColor, QFont, QPainter, QPen, QBrush, QLinearGradient
)
from PySide6.QtCore import Qt, QMargins, QDateTime, QPointF
from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
)
from models.mainModels.dashboard_model import DashboardModel
from presenters.mainPresenters.dashboard_presenter import DashboardPresenter

    # Called when user clicks "Add Money"
    def on_add_money(self):
        self.model.add_money(1000)
        self.update_view()

    # Called when user clicks "Remove Money"
    def on_remove_money(self):
        self.model.remove_money(1000)
        self.update_view()

    # Called when user clicks "Sell"
    def on_sell_stock(self, symbol):
        self.model.sell_stock(symbol)
        self.update_view()

# ---------------------------------------------------------------------
# 3) VIEW
# ---------------------------------------------------------------------
class SellButton(QPushButton):
    def __init__(self, text="Sell", parent=None):
        super().__init__(text, parent)
        self.setFixedSize(60, 24)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4D;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D43F3F;
            }
            QPushButton:pressed {
                background-color: #B53131;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #888888;
            }
        """)


class StockPerformanceChart(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.chart = QChart()
        self.chart.setTitle("Portfolio Performance")
        self.chart.setTitleFont(QFont("Arial", 14, QFont.Bold))
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(10, 10, 10, 10))

        self.series = QLineSeries()
        self.series.setName("Portfolio Value")
        pen = QPen(QColor("#5851DB"))
        pen.setWidth(3)
        self.series.setPen(pen)

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 300))
        gradient.setColorAt(0.0, QColor(88, 81, 219, 100))
        gradient.setColorAt(1.0, QColor(88, 81, 219, 0))
        self.series.setBrush(QBrush(gradient))

        self.axisX = QDateTimeAxis()
        self.axisX.setFormat("MMM yyyy")
        self.axisX.setTitleText("Date")
        self.axisX.setLabelsAngle(-45)
        self.axisX.setLabelsFont(QFont("Arial", 9))

        self.axisY = QValueAxis()
        self.axisY.setTitleText("Portfolio Value ($)")
        self.axisY.setLabelFormat("$%.0f")
        self.axisY.setLabelsFont(QFont("Arial", 9))

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.chart.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

        self.setChart(self.chart)
        self.chart.setBackgroundBrush(QColor("white"))
        self.setMinimumHeight(350)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    def load_data(self, data):
        self.series.clear()
        if not data:
            return

        min_value = float('inf')
        max_value = float('-inf')

        for date, value in data:
            timestamp = int(date.timestamp() * 1000)
            self.series.append(timestamp, value)
            min_value = min(min_value, value)
            max_value = max(max_value, value)

        first_date = data[0][0]
        last_date = data[-1][0]
        self.axisX.setRange(first_date, last_date)

        padding = (max_value - min_value) * 0.1
        self.axisY.setRange(max(0, min_value - padding), max_value + padding)


class StatCard(QFrame):
    def __init__(self, title, value, subtitle=None, icon=None, color="#5851DB", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setStyleSheet("""
            #StatCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #EAEAEA;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(5)

        header_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 15px; font-weight: 500;")
        header_layout.addWidget(title_label)

        if icon:
            icon_label = QLabel()
            pixmap = QPixmap(icon)
            icon_label.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            header_layout.addWidget(icon_label)
        else:
            header_layout.addStretch()

        self.layout.addLayout(header_layout)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #000; font-size: 28px; font-weight: bold;")
        self.layout.addWidget(self.value_label)

        if subtitle:
            subtitle_layout = QHBoxLayout()
            arrow_label = QLabel()
            if "+" in subtitle:
                arrow_label.setText("↗")
                arrow_label.setStyleSheet(f"color: {color}; font-size: 18px;")
            elif "-" in subtitle:
                arrow_label.setText("↘")
                arrow_label.setStyleSheet("color: #F44336; font-size: 18px;")

            subtitle_text = QLabel(subtitle)
            subtitle_text.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: 500;")

            subtitle_layout.addWidget(arrow_label)
            subtitle_layout.addWidget(subtitle_text)
            subtitle_layout.addStretch()
            self.layout.addLayout(subtitle_layout)


class PortfolioValueCard(StatCard):
    def __init__(self, title, value, subtitle=None, icon=None, color="#5851DB", parent=None):
        super().__init__(title, value, subtitle, icon, color, parent)
        button_layout = QHBoxLayout()

        self.add_money_btn = QPushButton("Add Money")
        self.remove_money_btn = QPushButton("Remove Money")

        self.add_money_btn.setStyleSheet("""
            QPushButton {
                background-color: #4C6FFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3A5BCC;
            }
            QPushButton:pressed {
                background-color: #2D49A3;
            }
        """)

        self.remove_money_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4D;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D43F3F;
            }
            QPushButton:pressed {
                background-color: #B53131;
            }
        """)

        button_layout.addWidget(self.add_money_btn)
        button_layout.addWidget(self.remove_money_btn)
        self.layout.addLayout(button_layout)


class HoldingsTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HoldingsTable")
        self.setStyleSheet("""
            #HoldingsTable {
                background-color: white;
                border: none;
                gridline-color: #EAEAEA;
            }
            #HoldingsTable::item {
                padding: 5px;
            }
            #HoldingsTable QHeaderView::section {
                background-color: #F5F5F5;
                border: none;
                border-bottom: 1px solid #EAEAEA;
                padding: 8px;
                font-weight: bold;
                color: #333;
            }
            QTableView {
                alternate-background-color: #F9F9F9;
                background-color: white;
            }
        """)

        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "ID", "Symbol", "Quantity", "Current Price",
            "Total Value", "Total Gain", "Gain %", "Actions"
        ])

        header = self.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        self.setColumnWidth(7, 80)

        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.setMinimumHeight(400)

    def load_data(self, holdings):
        self.setRowCount(len(holdings))
        for row, holding in enumerate(holdings):
            # ID
            id_item = QTableWidgetItem(str(holding.Id))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 0, id_item)

            # Symbol
            symbol_item = QTableWidgetItem(holding.Symbol)
            symbol_item.setFont(QFont("Arial", 10, QFont.Bold))
            self.setItem(row, 1, symbol_item)

            # Quantity
            quantity_item = QTableWidgetItem(str(holding.Quantity))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 2, quantity_item)

            # Current Price
            price_item = QTableWidgetItem(f"${holding.CurrentPrice:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(row, 3, price_item)

            # Total Value
            value_item = QTableWidgetItem(f"${holding.TotalValue:.2f}")
            value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(row, 4, value_item)

            # Total Gain
            gain_item = QTableWidgetItem(f"${holding.TotalGain:.2f}")
            gain_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if holding.TotalGain > 0:
                gain_item.setForeground(QColor("#4CAF50"))
            elif holding.TotalGain < 0:
                gain_item.setForeground(QColor("#F44336"))
            self.setItem(row, 5, gain_item)

            # Gain %
            gain_pct_item = QTableWidgetItem(f"{holding.TotalGainPercentage:.2f}%")
            gain_pct_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if holding.TotalGainPercentage > 0:
                gain_pct_item.setForeground(QColor("#4CAF50"))
            elif holding.TotalGainPercentage < 0:
                gain_pct_item.setForeground(QColor("#F44336"))
            self.setItem(row, 6, gain_pct_item)

            # Sell button
            sell_button = SellButton("Sell")
            # We'll let the view handle the click and call the presenter
            # so we store the symbol in the button's property:
            sell_button.clicked.connect(lambda _, sym=holding.Symbol: self.parent().on_sell_clicked(sym))
            self.setCellWidget(row, 7, sell_button)


class Dashboard_view(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def set_presenter(self, presenter):
        """Assign the presenter so the view can call it on user actions."""
        self.presenter = presenter

    def init_ui(self):
        self.setWindowTitle("Portfolio Dashboard")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial', sans-serif;
                background-color: #F7F8FA;
            }
            QLabel#PageTitle {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
            QLabel#SectionTitle {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-top: 20px;
            }
            QComboBox {
                padding: 5px 10px;
                border: 1px solid #EAEAEA;
                border-radius: 4px;
                background-color: white;
            }
        """)

        main_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        container = QWidget()
        self.scroll_area.setWidget(container)

        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(20, 20, 20, 20)
        self.container_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Portfolio Dashboard")
        title_label.setObjectName("PageTitle")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        period_label = QLabel("Period:")
        period_label.setStyleSheet("font-size: 14px; color: #666;")
        self.period_selector = QComboBox()
        self.period_selector.addItems(["Last 3 Months", "Last 6 Months", "Last Year", "All Time"])
        # On change, we notify the presenter
        self.period_selector.currentTextChanged.connect(self.on_period_changed)

        header_layout.addWidget(period_label)
        header_layout.addWidget(self.period_selector)
        self.container_layout.addLayout(header_layout)

        # Chart
        self.chart = StockPerformanceChart()
        self.container_layout.addWidget(self.chart)

        self.container_layout.addSpacing(30)

        # Stat cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.total_value_card = PortfolioValueCard("Total Portfolio Value", "$0", "+0%", color="#5851DB")
        self.total_gain_card = StatCard("Total Gain", "$0", "+0%", color="#4CAF50")
        self.total_gain_pct_card = StatCard("Gain Percentage", "0%", "+0%", color="#4CAF50")

        stats_layout.addWidget(self.total_value_card)
        stats_layout.addWidget(self.total_gain_card)
        stats_layout.addWidget(self.total_gain_pct_card)

        self.container_layout.addLayout(stats_layout)

        # Connect add/remove money signals
        self.total_value_card.add_money_btn.clicked.connect(self.on_add_money_clicked)
        self.total_value_card.remove_money_btn.clicked.connect(self.on_remove_money_clicked)

        # Holdings Table
        holdings_label = QLabel("My Holdings")
        holdings_label.setObjectName("SectionTitle")
        self.container_layout.addWidget(holdings_label)

        self.holdings_table = HoldingsTable(self)
        self.container_layout.addWidget(self.holdings_table)

        self.container_layout.addSpacing(40)

    # View → Presenter: "Period changed"
    def on_period_changed(self, text):
        if self.presenter:
            self.presenter.on_period_changed(text)

    # View → Presenter: "Add money"
    def on_add_money_clicked(self):
        if self.presenter:
            self.presenter.on_add_money()

    # View → Presenter: "Remove money"
    def on_remove_money_clicked(self):
        if self.presenter:
            self.presenter.on_remove_money()

    # View → Presenter: "Sell"
    def on_sell_clicked(self, symbol):
        if self.presenter:
            self.presenter.on_sell_stock(symbol)

    # Presenter → View: set holdings data
    def set_holdings_data(self, holdings):
        self.holdings_table.load_data(holdings)

    # Presenter → View: set chart data
    def set_chart_data(self, data):
        self.chart.load_data(data)

    # Presenter → View: set stats
    def set_portfolio_summary(self, total_value, total_gain, total_gain_pct):
        self.total_value_card.value_label.setText(f"${total_value:,.2f}")
        self.total_gain_card.value_label.setText(f"${total_gain:,.2f}")
        self.total_gain_pct_card.value_label.setText(f"{total_gain_pct:.2f}%")

# ---------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    
    # Instantiate Model & View
    model = PortfolioModel()
    view = Dashboard_view()
    
    # Instantiate Presenter
    presenter = DashboardPresenter(model, view)
    
    # Show the UI
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
