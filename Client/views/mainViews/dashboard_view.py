import datetime
import sys

sys.path.append('..')

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QHeaderView, QTableWidgetItem, QTableWidget
)

from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt, QDateTime

# Import custom components
from PySide6.QtCharts import QLineSeries, QDateTimeAxis, QValueAxis

from Client.views.components.styled_widgets import (
    ScrollableContainer, StyledLineSeriesChart, StyledStatsCard, StyledTable,
    PageTitleLabel, SectionTitleLabel, StyledLabel, PrimaryButton, DangerButton,
    SellButton
)


class PortfolioValueCard(StyledStatsCard):
    def __init__(self, title, value, subtitle=None, icon=None, color="#5851DB", parent=None):
        super().__init__(title, value, subtitle, icon, color, parent)
        button_layout = QHBoxLayout()

        self.add_money_btn = PrimaryButton("Add Money")
        self.remove_money_btn = DangerButton("Remove Money")

        button_layout.addWidget(self.add_money_btn)
        button_layout.addWidget(self.remove_money_btn)
        self.layout.addLayout(button_layout)


class HoldingsTable(StyledTable):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([
            "ID", "Symbol", "Quantity", "Current Price",
            "Total Value", "Total Gain", "Gain %", "Actions"
        ])

        self.setColumnWidth(0, 30)  # ID
        self.setColumnWidth(1, 150)  # Symbol
        self.setColumnWidth(2, 100)  # Quantity
        self.setColumnWidth(3, 140)  # Current Price
        self.setColumnWidth(4, 140)  # Total Value
        self.setColumnWidth(5, 140)  # Total Gain
        self.setColumnWidth(6, 120)  # Gain %
        self.setColumnWidth(7, 80)  # Actions

        header = self.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Fixed)

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
            symbol_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 1, symbol_item)

            # Quantity
            quantity_item = QTableWidgetItem(str(holding.Quantity))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 2, quantity_item)

            # Current Price
            price_item = QTableWidgetItem(f"${holding.CurrentPrice:.2f}")
            price_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 3, price_item)

            # Total Value
            value_item = QTableWidgetItem(f"${holding.TotalValue:.2f}")
            value_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 4, value_item)

            # Total Gain
            gain_item = QTableWidgetItem(f"${holding.TotalGain:.2f}")
            gain_item.setTextAlignment(Qt.AlignCenter)
            if holding.TotalGain > 0:
                gain_item.setForeground(QColor("#4CAF50"))
            elif holding.TotalGain < 0:
                gain_item.setForeground(QColor("#F44336"))
            self.setItem(row, 5, gain_item)

            # Gain %
            gain_pct_item = QTableWidgetItem(f"{holding.TotalGainPercentage:.2f}%")
            gain_pct_item.setTextAlignment(Qt.AlignCenter)
            if holding.TotalGainPercentage > 0:
                gain_pct_item.setForeground(QColor("#4CAF50"))
            elif holding.TotalGainPercentage < 0:
                gain_pct_item.setForeground(QColor("#F44336"))
            self.setItem(row, 6, gain_pct_item)

            # Sell button
            sell_button = SellButton("Sell")
            sell_button.clicked.connect(lambda _, sym=holding.Symbol: self.parent().on_sell_clicked(sym))
            self.setCellWidget(row, 7, sell_button)


class PortfolioChart(StyledLineSeriesChart):
    def __init__(self, parent=None):
        super().__init__("Portfolio Performance", color="#5851DB", parent=parent)
        self.setMinimumHeight(350)

        # Configure axes - first remove any existing axes
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        # Then add new axes
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
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

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


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.presenter = None  # Presenter will be set later
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Portfolio Dashboard")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial', sans-serif;
                background-color: #F7F8FA;
            }
            QComboBox {
                padding: 5px 10px;
                border: 1px solid #EAEAEA;
                border-radius: 4px;
                background-color: white;
            }
        """)

        main_layout = QVBoxLayout(self)
        self.scrollable_container = ScrollableContainer(self)
        main_layout.addWidget(self.scrollable_container)

        container = self.scrollable_container.widget()
        self.container_layout = self.scrollable_container.layout

        # Header
        header_layout = QHBoxLayout()
        title_label = PageTitleLabel("Portfolio Dashboard")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        period_label = StyledLabel("Period:", size=14, color="#666")
        self.period_selector = QComboBox()
        self.period_selector.addItems(["Last 3 Months", "Last 6 Months", "Last Year", "All Time"])
        self.period_selector.currentTextChanged.connect(self.on_period_changed)

        header_layout.addWidget(period_label)
        header_layout.addWidget(self.period_selector)
        self.container_layout.addLayout(header_layout)

        # Chart
        self.chart = PortfolioChart()
        self.container_layout.addWidget(self.chart)

        self.container_layout.addSpacing(30)

        # Stat cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        self.total_value_card = PortfolioValueCard("Total Portfolio Value", "$0", "+0%", color="#5851DB")
        self.total_gain_card = StyledStatsCard("Total Gain", "$0", "+0%", color="#4CAF50")
        self.total_gain_pct_card = StyledStatsCard("Gain Percentage", "0%", "+0%", color="#4CAF50")

        stats_layout.addWidget(self.total_value_card)
        stats_layout.addWidget(self.total_gain_card)
        stats_layout.addWidget(self.total_gain_pct_card)

        self.container_layout.addLayout(stats_layout)

        self.total_value_card.add_money_btn.clicked.connect(self.on_add_money_clicked)
        self.total_value_card.remove_money_btn.clicked.connect(self.on_remove_money_clicked)

        # Holdings Table
        holdings_label = SectionTitleLabel("My Holdings")
        self.container_layout.addWidget(holdings_label)

        self.holdings_table = HoldingsTable(self)
        self.container_layout.addWidget(self.holdings_table)

        self.container_layout.addSpacing(40)

    def on_period_changed(self, text):
        if self.presenter:
            self.presenter.on_period_changed(text)

    def on_add_money_clicked(self):
        if self.presenter:
            self.presenter.on_add_money()

    def on_remove_money_clicked(self):
        if self.presenter:
            self.presenter.on_remove_money()

    def on_sell_clicked(self, symbol):
        if self.presenter:
            self.presenter.on_sell_stock(symbol)

    def set_holdings_data(self, holdings):
        self.holdings_table.load_data(holdings)

    def set_chart_data(self, data):
        self.chart.load_data(data)

    def set_portfolio_summary(self, total_value, total_gain, total_gain_pct):
        self.total_value_card.value_label.setText(f"${total_value:,.2f}")
        self.total_gain_card.value_label.setText(f"${total_gain:,.2f}")
        self.total_gain_pct_card.value_label.setText(f"{total_gain_pct:.2f}%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = DashboardView()
    view.show()
    sys.exit(app.exec())
