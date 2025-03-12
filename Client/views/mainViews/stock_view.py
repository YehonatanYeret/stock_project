from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QLineEdit, QMessageBox, QFrame, QScrollArea, QGridLayout,
    QSplitter
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from views.components.styled_widgets import (
    StyledButton, ContentCard, PageHeader, SectionTitle
)
from views.components.chart import StockPerformanceChart


class StockView(QWidget):
    """Stock view displaying market data and stock search functionality"""
    
    # Signals
    search_stock_requested = Signal(str)
    add_to_watchlist_requested = Signal(str)
    remove_from_watchlist_requested = Signal(str)
    buy_stock_requested = Signal(str, float, float)
    refresh_data_requested = Signal()
    view_stock_details_requested = Signal(str)
    
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
        self.header = PageHeader("Stocks", "Search and analyze stocks")
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
        
        # Search section
        self.search_card = ContentCard("Search Stocks")
        
        self.search_layout = QHBoxLayout()
        self.search_layout.setSpacing(10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter stock symbol or company name...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #DEDEDE;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        
        self.search_button = StyledButton("Search")
        self.search_button.clicked.connect(self.on_search)
        
        # Connect enter key in search input to search button
        self.search_input.returnPressed.connect(self.on_search)
        
        self.search_layout.addWidget(self.search_input, 3)
        self.search_layout.addWidget(self.search_button, 1)
        
        self.search_card.content_layout.addLayout(self.search_layout)
        self.scroll_layout.addWidget(self.search_card)
        
        # Split view for details and watchlist
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        
        # Stock details section
        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setContentsMargins(0, 0, 10, 0)
        self.details_layout.setSpacing(20)
        
        # Stock details card (initially hidden)
        self.details_card = ContentCard("Stock Details")
        self.details_card.setVisible(False)
        
        # Stock info grid
        self.info_grid = QGridLayout()
        self.info_grid.setColumnStretch(0, 1)
        self.info_grid.setColumnStretch(1, 2)
        self.info_grid.setColumnStretch(2, 1)
        self.info_grid.setColumnStretch(3, 2)
        
        # Create labels for stock details
        self.company_name_label = QLabel("Company:")
        self.company_name = QLabel()
        self.company_name.setStyleSheet("font-weight: bold;")
        
        self.current_price_label = QLabel("Current Price:")
        self.current_price = QLabel()
        self.current_price.setStyleSheet("font-weight: bold; font-size: 18px; color: #4C6FFF;")
        
        self.change_label = QLabel("Change:")
        self.change = QLabel()
        
        self.open_label = QLabel("Open:")
        self.open_price = QLabel()
        
        self.high_label = QLabel("High:")
        self.high_price = QLabel()
        
        self.low_label = QLabel("Low:")
        self.low_price = QLabel()
        
        self.volume_label = QLabel("Volume:")
        self.volume = QLabel()
        
        self.market_cap_label = QLabel("Market Cap:")
        self.market_cap = QLabel()
        
        self.pe_ratio_label = QLabel("P/E Ratio:")
        self.pe_ratio = QLabel()
        
        self.dividend_label = QLabel("Dividend Yield:")
        self.dividend = QLabel()
        
        # Add labels to grid
        row = 0
        self.info_grid.addWidget(self.company_name_label, row, 0)
        self.info_grid.addWidget(self.company_name, row, 1)
        self.info_grid.addWidget(self.current_price_label, row, 2)
        self.info_grid.addWidget(self.current_price, row, 3)
        
        row += 1
        self.info_grid.addWidget(self.change_label, row, 0)
        self.info_grid.addWidget(self.change, row, 1)
        self.info_grid.addWidget(self.volume_label, row, 2)
        self.info_grid.addWidget(self.volume, row, 3)
        
        row += 1
        self.info_grid.addWidget(self.open_label, row, 0)
        self.info_grid.addWidget(self.open_price, row, 1)
        self.info_grid.addWidget(self.market_cap_label, row, 2)
        self.info_grid.addWidget(self.market_cap, row, 3)
        
        row += 1
        self.info_grid.addWidget(self.high_label, row, 0)
        self.info_grid.addWidget(self.high_price, row, 1)
        self.info_grid.addWidget(self.pe_ratio_label, row, 2)
        self.info_grid.addWidget(self.pe_ratio, row, 3)
        
        row += 1
        self.info_grid.addWidget(self.low_label, row, 0)
        self.info_grid.addWidget(self.low_price, row, 1)
        self.info_grid.addWidget(self.dividend_label, row, 2)
        self.info_grid.addWidget(self.dividend, row, 3)
        
        self.details_card.content_layout.addLayout(self.info_grid)
        
        # Action buttons
        self.action_layout = QHBoxLayout()
        self.action_layout.setSpacing(10)
        
        self.buy_button = StyledButton("Buy Stock")
        self.buy_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.buy_button.clicked.connect(self.on_buy_stock)
        
        self.watchlist_button = StyledButton("Add to Watchlist")
        self.watchlist_button.clicked.connect(self.on_toggle_watchlist)
        
        self.action_layout.addWidget(self.buy_button)
        self.action_layout.addWidget(self.watchlist_button)
        
        self.details_card.content_layout.addLayout(self.action_layout)
        self.details_layout.addWidget(self.details_card)
        
        # Stock chart card
        self.chart_card = ContentCard("Price History")
        self.chart_card.setVisible(False)
        
        # Time period selector
        self.period_layout = QHBoxLayout()
        self.period_label = QLabel("Time Period:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(["1 Day", "1 Week", "1 Month", "3 Months", "6 Months", "1 Year"])
        self.period_combo.setCurrentIndex(3)  # Default to 3 Months
        self.period_combo.currentIndexChanged.connect(self.on_period_changed)
        
        self.period_layout.addWidget(self.period_label)
        self.period_layout.addWidget(self.period_combo)
        self.period_layout.addStretch()
        
        self.chart_card.content_layout.addLayout(self.period_layout)
        
        # Stock price chart
        self.stock_chart = StockChart("Stock Price", "$")
        self.chart_card.content_layout.addWidget(self.stock_chart)
        
        self.details_layout.addWidget(self.chart_card)
        
        # Buy stock form (initially hidden)
        self.buy_card = ContentCard("Buy Stock")
        self.buy_card.setVisible(False)
        
        self.buy_grid = QGridLayout()
        self.buy_grid.setColumnStretch(0, 1)
        self.buy_grid.setColumnStretch(1, 3)
        
        self.shares_label = QLabel("Number of Shares:")
        self.shares_input = QLineEdit()
        self.shares_input.setPlaceholderText("Enter number of shares")
        
        self.price_label = QLabel("Current Market Price:")
        self.price_display = QLabel("$0.00")
        self.price_display.setStyleSheet("font-weight: bold; color: #4C6FFF;")
        
        self.total_label = QLabel("Total Cost:")
        self.total_display = QLabel("$0.00")
        self.total_display.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        self.buy_grid.addWidget(self.shares_label, 0, 0)
        self.buy_grid.addWidget(self.shares_input, 0, 1)
        self.buy_grid.addWidget(self.price_label, 1, 0)
        self.buy_grid.addWidget(self.price_display, 1, 1)
        self.buy_grid.addWidget(self.total_label, 2, 0)
        self.buy_grid.addWidget(self.total_display, 2, 1)
        
        self.buy_card.content_layout.addLayout(self.buy_grid)
        
        # Connect signals for real-time calculation
        self.shares_input.textChanged.connect(self.update_total_cost)
        
        # Confirm and cancel buttons
        self.buy_buttons_layout = QHBoxLayout()
        self.buy_buttons_layout.setSpacing(10)
        
        self.confirm_button = StyledButton("Confirm Purchase")
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.confirm_button.clicked.connect(self.on_confirm_purchase)
        
        self.cancel_button = StyledButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel_purchase)
        
        self.buy_buttons_layout.addWidget(self.cancel_button)
        self.buy_buttons_layout.addWidget(self.confirm_button)
        
        self.buy_card.content_layout.addLayout(self.buy_buttons_layout)
        self.details_layout.addWidget(self.buy_card)
        
        # Add stretch to push everything to the top
        self.details_layout.addStretch()
        
        # Watchlist section
        self.watchlist_widget = QWidget()
        self.watchlist_layout = QVBoxLayout(self.watchlist_widget)
        self.watchlist_layout.setContentsMargins(10, 0, 0, 0)
        self.watchlist_layout.setSpacing(20)
        
        # Watchlist card
        self.watchlist_card = ContentCard("Your Watchlist")
        
        # Watchlist table
        self.watchlist_table = QTableWidget()
        self.watchlist_table.setColumnCount(5)
        self.watchlist_table.setHorizontalHeaderLabels([
            "Symbol", "Name", "Price", "Change", "Actions"
        ])
        
        # Set table styling
        self.watchlist_table.setStyleSheet("""
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
        header = self.watchlist_table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.watchlist_table.setColumnWidth(4, 100)
        
        self.watchlist_card.content_layout.addWidget(self.watchlist_table)
        self.watchlist_layout.addWidget(self.watchlist_card)
        
        # Market indices card
        self.indices_card = ContentCard("Market Indices")
        
        # Indices grid
        self.indices_grid = QGridLayout()
        
        # Create index labels
        self.sp500_label = QLabel("S&P 500")
        self.sp500_label.setStyleSheet("font-weight: bold;")
        self.sp500_value = QLabel()
        self.sp500_change = QLabel()
        
        self.dow_label = QLabel("Dow Jones")
        self.dow_label.setStyleSheet("font-weight: bold;")
        self.dow_value = QLabel()
        self.dow_change = QLabel()
        
        self.nasdaq_label = QLabel("NASDAQ")
        self.nasdaq_label.setStyleSheet("font-weight: bold;")
        self.nasdaq_value = QLabel()
        self.nasdaq_change = QLabel()
        
        # Add index labels to grid
        row = 0
        self.indices_grid.addWidget(self.sp500_label, row, 0)
        self.indices_grid.addWidget(self.sp500_value, row, 1)
        self.indices_grid.addWidget(self.sp500_change, row, 2)

        row += 1
        self.indices_grid.addWidget(self.dow_label, row, 0)
        self.indices_grid.addWidget(self.dow_value, row, 1)
        self.indices_grid.addWidget(self.dow_change, row, 2)

        row += 1
        self.indices_grid.addWidget(self.nasdaq_label, row, 0)
        self.indices_grid.addWidget(self.nasdaq_value, row, 1)
        self.indices_grid.addWidget(self.nasdaq_change, row, 2)

        self.indices_card.content_layout.addLayout(self.indices_grid)
        self.watchlist_layout.addWidget(self.indices_card)

        # Add widgets to splitter
        self.splitter.addWidget(self.details_widget)
        self.splitter.addWidget(self.watchlist_widget)

        self.scroll_layout.addWidget(self.splitter)

    def on_search(self):
        """Emit signal with search query"""
        search_query = self.search_input.text().strip()
        if search_query:
            self.search_stock_requested.emit(search_query)
        else:
            QMessageBox.information(self, "Search", "Please enter a stock symbol or company name to search")

    def on_period_changed(self, index):
        """Emit signal with selected period index"""
        self.refresh_data_requested.emit()

    def on_buy_stock(self):
        """Show buy stock form"""
        self.buy_card.setVisible(True)
        self.buy_button.setVisible(False)
        self.watchlist_button.setVisible(False)

    def on_toggle_watchlist(self):
        """Toggle watchlist status"""
        if self.watchlist_button.text() == "Add to Watchlist":
            self.add_to_watchlist_requested.emit(self.stock_id)
        else:
            self.remove_from_watchlist_requested.emit(self.stock_id)


    def on_confirm_purchase(self):
        """Handle buy stock confirmation"""
        shares = self.shares_input.text().strip()
        if shares:
            self.buy_stock_requested.emit(self.stock_id, float(shares), self.current_price)
        else:
            QMessageBox.information(self, "Buy Stock", "Please enter the number of shares to purchase")

    def on_cancel_purchase(self):
        """Hide buy stock form"""
        self.buy_card.setVisible(False)
        self.buy_button.setVisible(True)
        self.watchlist_button.setVisible(True)

    def update_total_cost(self):
        """Update total cost based on number of shares"""
        shares = self.shares_input.text().strip()
        if shares:
            total_cost = float(shares) * self.current_price
            self.total_display.setText(f"${total_cost:.2f}")
        else:
            self.total_display.setText("$0.00")

    def show_error(self, message):
        """Display an error message"""
        QMessageBox.critical(self, "Error", message)

    def update_stock_details(self, stock_data):
        """Update stock details with new data"""
        self.stock_id = stock_data.get("symbol")
        self.company_name.setText(stock_data.get("name"))
        self.current_price.setText(f"${stock_data.get('price', 0):,.2f}")
        self.change.setText(stock_data.get("change", ""))
        self.open_price.setText(f"${stock_data.get('open', 0):,.2f}")
        self.high_price.setText(f"${stock_data.get('high', 0):,.2f}")
        self.low_price.setText(f"${stock_data.get('low', 0):,.2f}")
        self.volume.setText(f"{stock_data.get('volume', 0):,}")
        self.market_cap.setText(f"${stock_data.get('market_cap', 0):,.0f}")
        self.pe_ratio.setText(str(stock_data.get('pe_ratio', "")))
        self.dividend.setText(str(stock_data.get('dividend_yield', "")))
        # Update watchlist button text
        if stock_data.get('watchlisted'):
            self.watchlist_button.setText("Remove from Watchlist")
        else:
            self.watchlist_button.setText("Add to Watchlist")
        # Update buy form price
        self.price_display.setText(f"${stock_data.get('price', 0):,.2f}")
        self.update_total_cost()

        
    def update_stock_chart(self, dates, values):
        """Update stock price chart with historical data"""
        self.stock_chart.plot(dates, values)

    def update_watchlist(self, watchlist_data):
        """Update watchlist table with new data"""
        self.watchlist_table.setRowCount(len(watchlist_data))
        for row, stock_data in enumerate(watchlist_data):
            symbol_item = QTableWidgetItem(stock_data.get("symbol"))
            name_item = QTableWidgetItem(stock_data.get("name"))
            price_item = QTableWidgetItem(f"${stock_data.get('price', 0):,.2f}")
            change_item = QTableWidgetItem(stock_data.get("change"))
            action_button = QPushButton("View")
            action_button.clicked.connect(lambda _, s=stock_data.get("symbol"): self.view_stock_details_requested.emit(s))
            self.watchlist_table.setItem(row, 0, symbol_item)
            self.watchlist_table.setItem(row, 1, name_item)
            self.watchlist_table.setItem(row, 2, price_item)
            self.watchlist_table.setItem(row, 3, change_item)
            self.watchlist_table.setCellWidget(row, 4, action_button)

    def update_market_indices(self, indices_data):
        """Update market indices with new data"""
        self.sp500_value.setText(f"${indices_data.get('sp500', 0):,.2f}")
        self.sp500_change.setText(indices_data.get('sp500_change', ""))
        self.dow_value.setText(f"${indices_data.get('dow', 0):,.2f}")
        self.dow_change.setText(indices_data.get('dow_change', ""))
        self.nasdaq_value.setText(f"${indices_data.get('nasdaq', 0):,.2f}")
        self.nasdaq_change.setText(indices_data.get('nasdaq_change', ""))

    def clear_search_input(self):
        """Clear the search input field"""
        self.search_input.clear()

    def clear_stock_details(self):
        """Clear the stock details view"""
        self.company_name.clear()

        self.current_price.clear()
        self.change.clear()
        self.open_price.clear()
        self.high_price.clear()
        self.low_price.clear()
        self.volume.clear()
        self.market_cap.clear()
        self.pe_ratio.clear()
        self.dividend.clear()
        self.watchlist_button.setVisible(False)
        self.buy_button.setVisible(False)
        self.details_card.setVisible(False)
        self.chart_card.setVisible(False)
        self.buy_card.setVisible(False)

    def clear_watchlist(self):
        """Clear the watchlist table"""
        self.watchlist_table.setRowCount(0)


