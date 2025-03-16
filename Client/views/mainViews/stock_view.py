import sys

from PySide6.QtCore import Qt, Signal, QDate, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QIntValidator, QPalette, QLinearGradient, QGradient
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QDateEdit, QFrame, QSplitter, QScrollArea, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem, QMainWindow
)
from views.components.chart import StockChartWidget
from views.components.styled_widgets import (
    StyledLabel, StyledButton, StyledLineEdit, StyledDateEdit,
    PrimaryButton, Card, RoundedCard, GradientCard, ScrollableContainer,
    BuyToggleButton, SellToggleButton, PageTitleLabel, SectionTitleLabel,
    apply_shadow_effect, create_form_field, StyledChartView, StyledLineSeriesChart
)


class StockChart(RoundedCard):
    """Widget for displaying the stock price chart"""

    def __init__(self, parent=None):
        super().__init__(parent=parent, border_radius=12, shadow_enabled=True)
        self.setMinimumHeight(350)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        self.chart_container = RoundedCard(parent=self, border_radius=10, shadow_enabled=False)
        self.chart_container.setStyleSheet("QFrame {background-color: #F8FAFC;}")
        layout.addWidget(self.chart_container)

        # Embed StockChartWidget inside the container
        self.stock_chart_widget = StockChartWidget(self.chart_container)
        chart_layout = QVBoxLayout(self.chart_container)
        chart_layout.addWidget(self.stock_chart_widget)

    def update_chart(self, ticker, start_date, end_date, data):
        """Update chart with new stock data"""
        self.stock_chart_widget.update_chart(ticker, start_date, end_date, data)

    def clear_chart(self):
        """Clear chart data"""
        self.stock_chart_widget.clear_chart()


class StockView(QWidget):
    """Stock trading view for searching, analyzing, and trading stocks"""

    # Signals
    search_stock_requested = Signal(str, QDate, QDate)
    buy_stock_requested = Signal(str, int, float)
    sell_stock_requested = Signal(str, int, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    # python
    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.setMinimumSize(1000, 700)
        # self.main_layout.setSpacing(30)

        # Create scrollable content area
        self.scroll_area = ScrollableContainer(parent=self)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content_widget = self.scroll_area.widget()
        self.content_layout = self.scroll_area.layout  # Access the layout attribute directly

        # Create a search section
        self._create_search_section()

        # Create a stock info section
        self._create_stock_info_section()

        # Add the main scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

    def _create_scroll_area(self):
        """Create scrollable content area"""
        self.scroll_area = ScrollableContainer(self)
        self.content_widget = self.scroll_area.widget()
        self.content_layout = self.scroll_area.layout()

    def _create_search_section(self):
        """Create the search card section"""
        self.search_section = RoundedCard(parent=None, border_radius=16, shadow_enabled=True)

        search_layout = QVBoxLayout(self.search_section)
        search_layout.setContentsMargins(15, 15, 15, 15)
        search_layout.setSpacing(10)

        # Search title
        search_title = SectionTitleLabel("Search Stocks", parent=self.search_section)

        # Search form
        search_form = QHBoxLayout()
        search_form.setSpacing(10)

        # Stock Symbol input with StyledLineEdit
        symbol_input = StyledLineEdit(placeholder="Enter symbol", parent=self.search_section)
        self.symbol_input = symbol_input
        symbol_layout = create_form_field("Stock Symbol", symbol_input)

        # Start Date with StyledDateEdit
        start_date = StyledDateEdit(default_date=QDate(2024, 1, 1), parent=self.search_section)
        self.start_date = start_date
        start_date_layout = create_form_field("Start Date", start_date)

        # End Date with StyledDateEdit
        end_date = StyledDateEdit(default_date=QDate(2024, 1, 31), parent=self.search_section)
        self.end_date = end_date
        end_date_layout = create_form_field("End Date", end_date)

        # Add layouts to a search form
        search_form.addLayout(symbol_layout, 2)
        search_form.addLayout(start_date_layout, 2)
        search_form.addLayout(end_date_layout, 2)

        # Button layout
        button_layout = QHBoxLayout()
        self.search_button = PrimaryButton("Search", object_name="searchButton", parent=self.search_section)
        button_layout.addWidget(self.search_button)
        button_layout.addStretch(1)

        search_layout.addWidget(search_title)
        search_layout.addLayout(search_form)
        search_layout.addLayout(button_layout)

        # Add search section to content layout
        self.content_layout.addWidget(self.search_section)

    def _create_stock_info_section(self):
        """Create the stock information section"""
        self.stock_info_section = RoundedCard(parent=None, border_radius=16, shadow_enabled=True)

        stock_info_layout = QVBoxLayout(self.stock_info_section)
        stock_info_layout.setContentsMargins(15, 15, 15, 15)
        stock_info_layout.setSpacing(15)

        # Stock header with gradient card
        stock_header_card = self._create_stock_header_card()
        stock_info_layout.addWidget(stock_header_card)

        # Stock Chart
        self.chart = StockChart()

        # Main content area with buy/sell options
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

        # Right content - order panel
        right_content = QVBoxLayout()
        order_panel = self._create_order_panel()
        right_content.addWidget(order_panel)
        right_content.addStretch(1)

        content_layout.addWidget(self.chart, 3)
        content_layout.addLayout(right_content, 2)

        stock_info_layout.addLayout(content_layout)

        # Add stock info section to content layout
        self.content_layout.addWidget(self.stock_info_section)

    def _create_stock_header_card(self):
        """Create the stock header card with price information"""
        stock_header_card = GradientCard(
            parent=self.stock_info_section,
            start_color="#F0F9FF",
            end_color="#EFF6FF",
            border_color="#E0F2FE",
            shadow_enabled=False
        )

        stock_header_layout = QVBoxLayout(stock_header_card)
        stock_header_layout.setContentsMargins(20, 20, 20, 20)
        stock_header_layout.setSpacing(15)

        # Stock name and price
        stock_info = QVBoxLayout()

        self.stock_name = StyledLabel("", size=26, font_weight="bold", color="#0F172A", parent=stock_header_card)

        price_layout = QHBoxLayout()
        self.stock_price = StyledLabel("", size=36, font_weight="bold", color="#0F172A", parent=stock_header_card)

        self.stock_change = QLabel("")
        self.stock_change.setStyleSheet("""
            font-weight: bold;
            font-size: 18px;
            border-radius: 8px;
            padding: 5px 10px;
            margin-left: 10px;
        """)

        price_layout.addWidget(self.stock_price)
        price_layout.addWidget(self.stock_change)
        price_layout.addStretch(1)

        # Volume and Market Cap
        meta_layout = QHBoxLayout()

        self.volume_label = QLabel("")
        self.volume_label.setStyleSheet("""
            color: #64748B;
            font-size: 15px;
            background-color: #F1F5F9;
            border-radius: 8px;
            padding: 5px 15px;
        """)

        self.market_cap_label = QLabel("")
        self.market_cap_label.setStyleSheet("""
            color: #64748B;
            font-size: 15px;
            background-color: #F1F5F9;
            border-radius: 8px;
            padding: 5px 15px;
            margin-left: 10px;
        """)

        meta_layout.addWidget(self.volume_label)
        meta_layout.addWidget(self.market_cap_label)
        meta_layout.addStretch(1)

        stock_info.addWidget(self.stock_name)
        stock_info.addLayout(price_layout)
        stock_info.addLayout(meta_layout)

        stock_header_layout.addLayout(stock_info)

        return stock_header_card

    def _create_order_panel(self):
        """Create the order panel for buying/selling stocks"""
        order_panel = RoundedCard(parent=None, border_radius=16, shadow_enabled=True)
        # order_panel.setMinimumWidth(360)
        order_panel.setMaximumWidth(420)

        order_layout = QVBoxLayout(order_panel)
        order_layout.setContentsMargins(25, 25, 25, 25)
        order_layout.setSpacing(20)

        # Order header
        order_header = SectionTitleLabel("Place Order", parent=order_panel)

        # Order type
        order_type_label = StyledLabel("Order Type", size=15, font_weight="bold", color="#334155", parent=order_panel)

        # Buy/Sell buttons using BuyToggleButton and SellToggleButton
        order_type_buttons = QHBoxLayout()
        order_type_buttons.setSpacing(15)

        self.buy_button = BuyToggleButton(text="Buy", object_name="buyButton", is_checked=True, parent=order_panel)
        self.sell_button = SellToggleButton(text="Sell", object_name="sellButton", is_checked=False, parent=order_panel)

        order_type_buttons.addWidget(self.buy_button)
        order_type_buttons.addWidget(self.sell_button)

        # Quantity
        quantity_label = StyledLabel("Quantity", size=15, font_weight="bold", color="#334155", parent=order_panel)

        # Use StyledLineEdit instead
        self.quantity_input = StyledLineEdit(placeholder="Enter quantity", parent=order_panel)
        self.quantity_input.setText("1")
        self.quantity_input.setValidator(QIntValidator(1, 10000))

        # Price info card
        price_info_card = self._create_price_info_card()

        # Buy/Sell action button
        self.action_button = StyledButton(
            text="Buy",
            bg_color="#10B981",
            hover_color="#059669",
            pressed_color="#047857",
            text_color="white",
            border_radius=12,
            padding="12px",
            font_size=16,
            object_name="actionButton",
            parent=order_panel
        )
        self.action_button.setMinimumHeight(54)

        # Add widgets to order layout
        order_layout.addWidget(order_header)
        order_layout.addWidget(order_type_label)
        order_layout.addLayout(order_type_buttons)
        order_layout.addWidget(quantity_label)
        order_layout.addWidget(self.quantity_input)
        order_layout.addWidget(price_info_card)
        order_layout.addWidget(self.action_button)
        order_layout.addStretch(1)

        return order_panel

    def _create_price_info_card(self):
        """Create the price information card"""
        price_info_card = RoundedCard(parent=None, border_radius=10, shadow_enabled=False)
        price_info_card.setStyleSheet("QFrame {background-color: #F8FAFC; border: 1px solid #E2E8F0;}")

        price_info_layout = QVBoxLayout(price_info_card)
        price_info_layout.setContentsMargins(15, 15, 15, 15)
        price_info_layout.setSpacing(10)

        price_grid = QGridLayout()
        price_grid.setHorizontalSpacing(10)
        price_grid.setVerticalSpacing(12)

        price_label = StyledLabel("Market Price:", size=15, color="#64748B", parent=price_info_card)

        self.price_value = StyledLabel("$0.00", size=15, font_weight="bold", color="#0F172A", parent=price_info_card)
        self.price_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        total_label = StyledLabel("Total Value:", size=15, color="#64748B", parent=price_info_card)

        self.total_value = StyledLabel("$0.00", size=15, font_weight="bold", color="#0F172A", parent=price_info_card)
        self.total_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        price_grid.addWidget(price_label, 0, 0)
        price_grid.addWidget(self.price_value, 0, 1)
        price_grid.addWidget(total_label, 1, 0)
        price_grid.addWidget(self.total_value, 1, 1)

        price_info_layout.addLayout(price_grid)

        return price_info_card

    def _update_action_button(self, is_buy=True, symbol=""):
        """Update the action button style and text based on buy/sell status"""
        action_text = f"{'Buy' if is_buy else 'Sell'} {symbol}" if symbol else f"{'Buy' if is_buy else 'Sell'}"
        self.action_button.setText(action_text)

        # Update button colors based on buy/sell status
        if is_buy:
            self.action_button.setStyleSheet(f"""
                #actionButton {{
                    background-color: #10B981;
                    color: white;
                    border-radius: 12px;
                    font-weight: bold;
                    padding: 12px;
                    font-size: 16px;
                    border: none;
                }}
                #actionButton:hover {{
                    background-color: #059669;
                }}
                #actionButton:pressed {{
                    background-color: #047857;
                }}
            """)
        else:
            self.action_button.setStyleSheet(f"""
                #actionButton {{
                    background-color: #EF4444;
                    color: white;
                    border-radius: 12px;
                    font-weight: bold;
                    padding: 12px;
                    font-size: 16px;
                    border: none;
                }}
                #actionButton:hover {{
                    background-color: #DC2626;
                }}
                #actionButton:pressed {{
                    background-color: #B91C1C;
                }}
            """)

    def setup_connections(self):
        """Connect signals and slots"""
        # Search button
        self.search_button.clicked.connect(self.on_search)

        # Connect enter key in search input to search button
        self.symbol_input.returnPressed.connect(self.on_search)

        # Order type buttons
        self.buy_button.clicked.connect(self.on_order_type_changed)
        self.sell_button.clicked.connect(self.on_order_type_changed)

        # Quantity input
        self.quantity_input.textChanged.connect(self.update_total_value)

        # Action button
        self.action_button.clicked.connect(self.on_action_button_clicked)

    def on_search(self):
        """Handle search button click"""
        symbol = self.symbol_input.text().strip().upper()
        start_date = self.start_date.date()
        end_date = self.end_date.date()

        if symbol:
            self.search_stock_requested.emit(symbol, start_date, end_date)

    def on_order_type_changed(self):
        """Handle order type change"""
        symbol = self.symbol_input.text().upper() if self.symbol_input.text() else ""

        if self.sender() == self.buy_button and self.buy_button.isChecked():
            self.sell_button.setChecked(False)
            self._update_action_button(is_buy=True, symbol=symbol)
        elif self.sender() == self.sell_button and self.sell_button.isChecked():
            self.buy_button.setChecked(False)
            self._update_action_button(is_buy=False, symbol=symbol)

    def update_total_value(self):
        """Update total value based on quantity"""
        try:
            quantity = int(self.quantity_input.text()) if self.quantity_input.text() else 0
            price = float(self.price_value.text().replace('$', ''))
            total = quantity * price
            self.total_value.setText(f"${total:.2f}")
        except (ValueError, AttributeError):
            self.total_value.setText("$0.00")

    def on_action_button_clicked(self):
        """Handle buy/sell action"""
        try:
            symbol = self.symbol_input.text().strip().upper()
            quantity = int(self.quantity_input.text())
            price = float(self.price_value.text().replace('$', ''))

            if self.buy_button.isChecked():
                self.buy_stock_requested.emit(symbol, quantity, price)
            elif self.sell_button.isChecked():
                self.sell_stock_requested.emit(symbol, quantity, price)
        except (ValueError, AttributeError):
            pass  # Handle error in presenter

    def update_stock_data(self, symbol, start_date, end_date, stock_data):
        """Update stock information in the UI

        Args:
            :param stock_data:  - name: Company name
                               - symbol: Stock symbol
                               - volume: Trading volume
            :param end_date: end date
            :param symbol: stock symbol
            :param start_date: start date
        """
        # Update stock header
        self.stock_name.setText(f"{stock_data['name']} ({stock_data['symbol']})")

        # Format volume with commas
        formatted_volume = f"{stock_data['volume']:,}"
        self.volume_label.setText(f"Volume: {formatted_volume}")

        # Update action button text
        is_buy = self.buy_button.isChecked()
        self._update_action_button(is_buy=is_buy, symbol=stock_data['symbol'])

        # Update chart with provided stock data
        if 'chart_data' in stock_data:
            self.chart.update_chart(symbol, start_date, end_date, stock_data['chart_data'])

    def show_message(self, message, is_error=False):
        """Display a message to the user"""
        from PySide6.QtWidgets import QMessageBox

        message_box = QMessageBox()
        message_box.setText(message)

        if is_error:
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle("Error")
        else:
            message_box.setIcon(QMessageBox.Information)
            message_box.setWindowTitle("Success")

        message_box.exec()
