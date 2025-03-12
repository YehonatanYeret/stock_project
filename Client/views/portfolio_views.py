from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QLineEdit, QMessageBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtCharts import QChart, QChartView, QPieSeries

from views.components.styled_widgets import (
    StyledButton, ContentCard, PageHeader, SectionTitle
)
from views.components.chart import StockChart


class PortfolioView(QWidget):
    """Portfolio view displaying user's stock holdings and performance"""
    
    # Signals
    add_stock_requested = Signal(str, float, float)
    remove_stock_requested = Signal(str)
    refresh_data_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(20)
        
        # Page header
        self.header = PageHeader("Portfolio", "Manage your stock holdings")
        self.main_layout.addWidget(self.header)
        
        # Content area with scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        
        # Portfolio summary card
        self.summary_card = ContentCard("Portfolio Summary")
        self.summary_layout = QHBoxLayout()
        self.summary_card.content_layout.addLayout(self.summary_layout)
        
        # Portfolio metrics
        self.metrics_layout = QVBoxLayout()
        self.metrics_layout.setSpacing(16)
        
        self.total_value_label = QLabel("Total Value")
        self.total_value_label.setStyleSheet("font-weight: bold; color: #555;")
        self.total_value = QLabel("$0.00")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold; color: #4C6FFF;")
        
        self.metrics_layout.addWidget(self.total_value_label)
        self.metrics_layout.addWidget(self.total_value)
        
        self.total_gain_label = QLabel("Total Gain/Loss")
        self.total_gain_label.setStyleSheet("font-weight: bold; color: #555;")
        self.total_gain = QLabel("$0.00 (0.00%)")
        self.total_gain.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")
        
        self.metrics_layout.addWidget(self.total_gain_label)
        self.metrics_layout.addWidget(self.total_gain)
        
        self.metrics_layout.addStretch()
        self.summary_layout.addLayout(self.metrics_layout, 1)
        
        # Portfolio allocation chart
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_container)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        
        self.pie_series = QPieSeries()
        self.pie_chart = QChart()
        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setTitle("Portfolio Allocation")
        self.pie_chart.legend().setAlignment(Qt.AlignRight)
        self.pie_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.pie_chart.setTheme(QChart.ChartThemeLight)
        
        self.chart_view = QChartView(self.pie_chart)
        self.chart_view.setRenderHint(self.chart_view.RenderHint.Antialiasing)
        self.chart_layout.addWidget(self.chart_view)
        
        self.summary_layout.addWidget(self.chart_container, 2)
        self.scroll_layout.addWidget(self.summary_card)
        
        # Holdings table card
        self.holdings_card = ContentCard("Your Holdings")
        
        # Add stock section
        self.add_stock_layout = QHBoxLayout()
        self.add_stock_layout.setSpacing(10)
        
        self.stock_symbol_input = QLineEdit()
        self.stock_symbol_input.setPlaceholderText("Stock Symbol (e.g., AAPL)")
        self.stock_symbol_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
            }
        """)
        
        self.shares_input = QLineEdit()
        self.shares_input.setPlaceholderText("Shares")
        self.shares_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
            }
        """)
        
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Purchase Price")
        self.price_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
            }
        """)
        
        self.add_button = StyledButton("Add Stock")
        self.add_button.clicked.connect(self.on_add_stock)
        
        self.add_stock_layout.addWidget(self.stock_symbol_input, 1)
        self.add_stock_layout.addWidget(self.shares_input, 1)
        self.add_stock_layout.addWidget(self.price_input, 1)
        self.add_stock_layout.addWidget(self.add_button)
        
        self.holdings_card.content_layout.addLayout(self.add_stock_layout)
        
        # Holdings table
        self.holdings_table = QTableWidget()
        self.holdings_table.setColumnCount(8)
        self.holdings_table.setHorizontalHeaderLabels([
            "Symbol", "Name", "Shares", "Purchase Price", 
            "Current Price", "Market Value", "Gain/Loss", "Actions"
        ])
        
        # Set table styling
        self.holdings_table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Set column stretch
        header = self.holdings_table.horizontalHeader()
        for i in range(7):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        self.holdings_table.setColumnWidth(7, 100)
        
        self.holdings_card.content_layout.addWidget(self.holdings_table)
        self.scroll_layout.addWidget(self.holdings_card)
        
        # Performance chart card
        self.performance_card = ContentCard("Portfolio Performance")
        
        # Time period selector
        self.period_layout = QHBoxLayout()
        self.period_label = QLabel("Time Period:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "All Time"])
        self.period_combo.setCurrentIndex(3)  # Default to 6 Months
        self.period_combo.currentIndexChanged.connect(self.on_period_changed)
        
        self.period_layout.addWidget(self.period_label)
        self.period_layout.addWidget(self.period_combo)
        self.period_layout.addStretch()
        
        self.performance_card.content_layout.addLayout(self.period_layout)
        
        # Portfolio performance chart
        self.portfolio_chart = StockChart("Portfolio Value Over Time", "$")
        self.performance_card.content_layout.addWidget(self.portfolio_chart)
        
        self.scroll_layout.addWidget(self.performance_card)
        
        # Refresh button
        self.refresh_button = StyledButton("Refresh Data")
        self.refresh_button.clicked.connect(self.refresh_data_requested)
        self.scroll_layout.addWidget(self.refresh_button, 0, Qt.AlignRight)
        
        # Add stretch to push everything to the top
        self.scroll_layout.addStretch()
    
    def on_add_stock(self):
        """Handle add stock button click"""
        symbol = self.stock_symbol_input.text().strip().upper()
        
        try:
            shares = float(self.shares_input.text())
            price = float(self.price_input.text())
            
            if not symbol:
                QMessageBox.warning(self, "Input Error", "Please enter a stock symbol.")
                return
                
            if shares <= 0:
                QMessageBox.warning(self, "Input Error", "Shares must be greater than 0.")
                return
                
            if price <= 0:
                QMessageBox.warning(self, "Input Error", "Purchase price must be greater than 0.")
                return
            
            # Emit signal to add stock
            self.add_stock_requested.emit(symbol, shares, price)
            
            # Clear inputs
            self.stock_symbol_input.clear()
            self.shares_input.clear()
            self.price_input.clear()
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for shares and price.")
    
    def on_period_changed(self, index):
        """Handle time period change for performance chart"""
        periods = ["1w", "1m", "3m", "6m", "1y", "all"]
        if 0 <= index < len(periods):
            self.refresh_data_requested.emit()
    
    def update_portfolio_summary(self, total_value, total_gain, gain_percentage):
        """Update portfolio summary values"""
        self.total_value.setText(f"${total_value:,.2f}")
        
        gain_color = "#4CAF50" if total_gain >= 0 else "#F44336"
        gain_prefix = "+" if total_gain > 0 else ""
        
        self.total_gain.setText(f"{gain_prefix}${total_gain:,.2f} ({gain_prefix}{gain_percentage:.2f}%)")
        self.total_gain.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {gain_color};")
    
    def update_allocation_chart(self, allocations):
        """Update the portfolio allocation pie chart
        
        Args:
            allocations: List of (symbol, percentage) tuples
        """
        self.pie_series.clear()
        
        for symbol, percentage in allocations:
            slice = self.pie_series.append(f"{symbol} ({percentage:.1f}%)", percentage)
            slice.setLabelVisible(True)
    
    def update_holdings_table(self, holdings):
        """Update the holdings table with current data
        
        Args:
            holdings: List of dictionaries with stock holding data
        """
        self.holdings_table.setRowCount(0)
        
        for row, holding in enumerate(holdings):
            self.holdings_table.insertRow(row)
            
            # Create table items
            symbol_item = QTableWidgetItem(holding['symbol'])
            name_item = QTableWidgetItem(holding['name'])
            shares_item = QTableWidgetItem(f"{holding['shares']:,.2f}")
            purchase_price_item = QTableWidgetItem(f"${holding['purchase_price']:,.2f}")
            current_price_item = QTableWidgetItem(f"${holding['current_price']:,.2f}")
            market_value_item = QTableWidgetItem(f"${holding['market_value']:,.2f}")
            
            # Calculate gain/loss
            gain = holding['market_value'] - (holding['purchase_price'] * holding['shares'])
            gain_pct = (gain / (holding['purchase_price'] * holding['shares'])) * 100 if holding['purchase_price'] > 0 else 0
            
            gain_prefix = "+" if gain > 0 else ""
            gain_item = QTableWidgetItem(f"{gain_prefix}${gain:,.2f} ({gain_prefix}{gain_pct:.2f}%)")
            
            # Set colors for gain/loss
            if gain > 0:
                gain_item.setForeground(QColor("#4CAF50"))
            elif gain < 0:
                gain_item.setForeground(QColor("#F44336"))
            
            # Center align numeric values
            for item in [shares_item, purchase_price_item, current_price_item, market_value_item, gain_item]:
                item.setTextAlignment(Qt.AlignCenter)
            
            # Add items to the table
            self.holdings_table.setItem(row, 0, symbol_item)
            self.holdings_table.setItem(row, 1, name_item)
            self.holdings_table.setItem(row, 2, shares_item)
            self.holdings_table.setItem(row, 3, purchase_price_item)
            self.holdings_table.setItem(row, 4, current_price_item)
            self.holdings_table.setItem(row, 5, market_value_item)
            self.holdings_table.setItem(row, 6, gain_item)
            
            # Add remove button
            remove_button = QPushButton("Remove")
            remove_button.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                }
            """)
            
            # Use lambda with default argument to capture the current symbol
            remove_button.clicked.connect(lambda checked, s=holding['symbol']: self.remove_stock_requested.emit(s))
            
            self.holdings_table.setCellWidget(row, 7, remove_button)
    
    def update_performance_chart(self, dates, values):
        """Update the portfolio performance chart
        
        Args:
            dates: List of date strings
            values: List of portfolio values
        """
        self.portfolio_chart.clear_series()
        self.portfolio_chart.add_series("Portfolio Value", dates, values, "#4C6FFF")
        self.portfolio_chart.update_chart()
    
    def show_error(self, message):
        """Display an error message"""
        QMessageBox.critical(self, "Error", message)