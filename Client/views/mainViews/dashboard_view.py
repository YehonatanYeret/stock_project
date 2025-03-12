from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QMessageBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from views.components.styled_widgets import (
    PrimaryButton, SecondaryButton, ContentCard, PageHeader, SectionTitle, StyledLabel
)
from views.components.chart import StockChartWidget


class Dashboard_view(QWidget):
    """Dashboard view displaying performance and holdings with option to sell stocks."""
    
    remove_stock_requested = Signal(str)
    refresh_data_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_mock_data()  # Load mock data on initialization
    
    def init_ui(self):
        """Initialize UI components."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(20)
        
        # Page header
        self.header = PageHeader("Dashboard", "Overview of your portfolio")
        self.main_layout.addWidget(self.header)
        
        # Scrollable content area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        # ─── METRICS ROW ──────────────────────────────────────────────────
        self.metrics_row = QHBoxLayout()
        self.metrics_row.setSpacing(16)
        
        self.portfolio_value_card = self.create_metric_card("Portfolio Value", "$0.00", "+0.0% today")
        self.total_stocks_card = self.create_metric_card("Total Stocks", "0", "Across 0 companies")
        self.days_gain_card = self.create_metric_card("Day's Gain", "$0.00", "+0.0%")
        self.total_return_card = self.create_metric_card("Total Return", "$0.00", "+0.0% all time")
        
        self.metrics_row.addWidget(self.portfolio_value_card)
        self.metrics_row.addWidget(self.total_stocks_card)
        self.metrics_row.addWidget(self.days_gain_card)
        self.metrics_row.addWidget(self.total_return_card)
        self.scroll_layout.addLayout(self.metrics_row)
        
        # ─── PERFORMANCE CHART CARD ───────────────────────────────────────
        self.performance_card = ContentCard()
        self.performance_card_layout = QVBoxLayout(self.performance_card)
        self.performance_card_layout.setContentsMargins(20, 20, 20, 20)
        
        self.performance_title = SectionTitle("Portfolio Performance")
        self.performance_card_layout.addWidget(self.performance_title)
        
        # Time period selector
        self.period_layout = QHBoxLayout()
        self.period_label = QLabel("Time Period:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "All Time"])
        self.period_combo.setCurrentIndex(3)
        # self.period_combo.currentIndexChanged.connect(self.on_period_changed)
        self.period_layout.addWidget(self.period_label)
        self.period_layout.addWidget(self.period_combo)
        self.period_layout.addStretch()
        self.performance_card_layout.addLayout(self.period_layout)
        
        # Stock chart
        self.portfolio_chart = StockChartWidget()
        self.performance_card_layout.addWidget(self.portfolio_chart)
        self.scroll_layout.addWidget(self.performance_card)
        
        # ─── HOLDINGS TABLE ───────────────────────────────────────────────
        self.holdings_card = ContentCard()
        self.holdings_card_layout = QVBoxLayout(self.holdings_card)
        self.holdings_card_layout.setContentsMargins(20, 20, 20, 20)
        
        self.holdings_title = SectionTitle("Your Holdings")
        self.holdings_card_layout.addWidget(self.holdings_title)
        
        self.holdings_table = QTableWidget()
        self.holdings_table.setColumnCount(8)
        self.holdings_table.setHorizontalHeaderLabels([
            "Symbol", "Name", "Shares", "Purchase Price",
            "Current Price", "Market Value", "Gain/Loss", "Actions"
        ])
        
        # Styling: Remove borders and gray backgrounds
        self.holdings_table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: white;
                border: none;
                font-weight: bold;
                padding: 8px;
            }
            QTableWidget::item {
                border: none;
                padding: 6px;
            }
        """)
        
        # Column resizing
        header = self.holdings_table.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        self.holdings_table.setColumnWidth(7, 80)
        
        # Reduce table height
        self.holdings_table.setMinimumHeight(220)
        
        self.holdings_card_layout.addWidget(self.holdings_table)
        self.scroll_layout.addWidget(self.holdings_card)
        
        # ─── REFRESH BUTTON ───────────────────────────────────────────────
        self.refresh_button = PrimaryButton("Refresh Data")
        self.refresh_button.clicked.connect(self.refresh_data_requested)
        self.scroll_layout.addWidget(self.refresh_button, 0, Qt.AlignRight)
        self.scroll_layout.addStretch()
    
    def create_metric_card(self, title, main_text, sub_text):
        """Creates a simple metric card."""
        card = ContentCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        
        title_label = StyledLabel(text=title)
        title_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        main_label = StyledLabel(text=main_text)
        main_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        sub_label = StyledLabel(text=sub_text)
        sub_label.setStyleSheet("font-size: 13px;")
        
        layout.addWidget(title_label)
        layout.addWidget(main_label)
        layout.addWidget(sub_label)
        
        return card
    
    
    def load_mock_data(self):
        """Load mock data for performance and holdings."""
        # Update portfolio summary with mock values
        
        # Create mock performance data for the chart (list of dicts with 't' and 'c')
        import time
        current_time_ms = int(time.time() * 1000)
        mock_performance_data = []
        # Generate 30 days of data
        for i in range(30):
            t = current_time_ms - (29 - i) * 86400000  # one day in ms
            c = 140 + i * 0.5  # simple trend
            mock_performance_data.append({'t': t, 'c': c})
        
        # Call update_chart with only the data parameter
        try:
            # self.portfolio_chart.update_chart(mock_performance_data)
            pass
        except Exception as e:
            print("Error updating chart:", e)
        
        # Create mock holdings data
        mock_holdings = [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'shares': 50,
                'purchase_price': 130.00,
                'current_price': 145.00,
                'market_value': 50 * 145.00
            },
            {
                'symbol': 'GOOGL',
                'name': 'Alphabet Inc.',
                'shares': 10,
                'purchase_price': 1500.00,
                'current_price': 1550.00,
                'market_value': 10 * 1550.00
            },
            {
                'symbol': 'AMZN',
                'name': 'Amazon.com Inc.',
                'shares': 5,
                'purchase_price': 3100.00,
                'current_price': 3200.00,
                'market_value': 5 * 3200.00
            }
        ]
        self.update_holdings_table(mock_holdings)
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def update_holdings_table(self, holdings):
        self.holdings_table.setRowCount(0)
        for row, holding in enumerate(holdings):
            self.holdings_table.insertRow(row)
            
            symbol_item = QTableWidgetItem(holding['symbol'])
            name_item = QTableWidgetItem(holding.get('name', '—'))
            shares_item = QTableWidgetItem(f"{holding['shares']:,.2f}")
            purchase_price_item = QTableWidgetItem(f"${holding['purchase_price']:,.2f}")
            current_price_item = QTableWidgetItem(f"${holding['current_price']:,.2f}")
            market_value_item = QTableWidgetItem(f"${holding['market_value']:,.2f}")
            
            gain = holding['market_value'] - (holding['purchase_price'] * holding['shares'])
            gain_prefix = "+" if gain > 0 else ""
            gain_item = QTableWidgetItem(f"{gain_prefix}${gain:,.2f}")
            
            if gain > 0:
                gain_item.setForeground(QColor("#4CAF50"))
            elif gain < 0:
                gain_item.setForeground(QColor("#F44336"))
            
            # Sell button
            sell_button = QPushButton("Sell")
            sell_button.setFixedSize(60, 24)
            sell_button.clicked.connect(lambda checked, s=holding['symbol']: self.remove_stock_requested.emit(s))
            
            self.holdings_table.setItem(row, 0, symbol_item)
            self.holdings_table.setItem(row, 1, name_item)
            self.holdings_table.setCellWidget(row, 7, sell_button)
