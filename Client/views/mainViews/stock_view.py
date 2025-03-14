import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QDateEdit, QFrame, QSplitter, QScrollArea, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem, QMainWindow
)
from PySide6.QtCore import Qt, Signal, QDate, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QIntValidator, QPalette, QLinearGradient, QGradient


class StockChart(QFrame):
    """widget for displaying the stock price chart"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(350)
        self.setObjectName("chartFrame")
        self.setStyleSheet("#chartFrame {background-color: white; border: 1px solid #E4E7EC; border-radius: 12px;}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.chart_container = QFrame(self)
        self.chart_container.setStyleSheet("QFrame {background-color: #F8FAFC; border-radius: 10px;}")
        layout.addWidget(self.chart_container)

    def update_chart(self, data):
        """Update chart with new stock data
        Args:
            data: Dictionary containing chart data points
        """
        # This would be implemented with a real charting library
        pass


class StockTradingView(QWidget):
    """Stock trading view for searching, analyzing, and trading stocks"""

    # Signals
    search_stock_requested = Signal(str, QDate, QDate)
    buy_stock_requested = Signal(str, int, float)
    sell_stock_requested = Signal(str, int, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        """Initialize the UI components"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(25)

        # Set window styles
        self._set_global_styles()

        # Create scrollable content area
        self._create_scroll_area()

        # Create search section
        self._create_search_section()

        # Create stock info section
        self._create_stock_info_section()

        # Add the main scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

    def _set_global_styles(self):
        """Set global stylesheet for the application"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F1F5F9;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #334155;
            }
        """)

    def _create_scroll_area(self):
        """Create scrollable content area"""
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #E2E8F0;
                width: 14px;
                margin: 0px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #94A3B8;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748B;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Create content widget for scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(25)

        self.scroll_area.setWidget(self.content_widget)

    def _create_search_section(self):
        """Create the search card section"""
        self.search_section = QFrame()
        self.search_section.setObjectName("searchCard")
        self._apply_shadow_effect(self.search_section)
        self.search_section.setStyleSheet("#searchCard {background-color: white; border-radius: 16px; border: none;}")

        search_layout = QVBoxLayout(self.search_section)
        search_layout.setContentsMargins(25, 25, 25, 25)
        search_layout.setSpacing(20)

        # Search title
        search_title = self._create_styled_label("Search Stocks", font_size=20, is_bold=True, color="#0F172A")

        # Search form
        search_form = QHBoxLayout()
        search_form.setSpacing(20)

        # Stock Symbol
        symbol_layout = self._create_form_field("Stock Symbol", "symbol_input", placeholder="Enter symbol")

        # Start Date
        start_date_layout = self._create_date_field("Start Date", "start_date", QDate(2024, 1, 1))

        # End Date
        end_date_layout = self._create_date_field("End Date", "end_date", QDate(2024, 1, 31))

        # Add layouts to search form
        search_form.addLayout(symbol_layout, 2)
        search_form.addLayout(start_date_layout, 2)
        search_form.addLayout(end_date_layout, 2)

        # Button layout
        button_layout = QHBoxLayout()
        self.search_button = self._create_primary_button("Search", "searchButton")
        button_layout.addWidget(self.search_button)
        button_layout.addStretch(1)

        search_layout.addWidget(search_title)
        search_layout.addLayout(search_form)
        search_layout.addLayout(button_layout)

        # Add search section to content layout
        self.content_layout.addWidget(self.search_section)

    def _create_stock_info_section(self):
        """Create the stock information section"""
        self.stock_info_section = QFrame()
        self.stock_info_section.setObjectName("stockInfoCard")
        self._apply_shadow_effect(self.stock_info_section)
        self.stock_info_section.setStyleSheet(
            "#stockInfoCard {background-color: white; border-radius: 16px; border: none;}")

        stock_info_layout = QVBoxLayout(self.stock_info_section)
        stock_info_layout.setContentsMargins(25, 25, 25, 25)
        stock_info_layout.setSpacing(25)

        # Stock header with gradient card
        stock_header_card = self._create_stock_header_card()
        stock_info_layout.addWidget(stock_header_card)

        # Stock Chart
        self.chart = StockChart()
        stock_info_layout.addWidget(self.chart)

        # Main content area with buy/sell options
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)

        # Left content - stats card
        left_content = QVBoxLayout()
        stats_card = self._create_stats_card()
        left_content.addWidget(stats_card)
        left_content.addStretch(1)

        # Right content - order panel
        right_content = QVBoxLayout()
        order_panel = self._create_order_panel()
        right_content.addWidget(order_panel)
        right_content.addStretch(1)

        content_layout.addLayout(left_content, 3)
        content_layout.addLayout(right_content, 2)

        stock_info_layout.addLayout(content_layout)

        # Add stock info section to content layout
        self.content_layout.addWidget(self.stock_info_section)

    def _create_stock_header_card(self):
        """Create the stock header card with price information"""
        stock_header_card = QFrame()
        stock_header_card.setObjectName("stockHeaderCard")
        stock_header_card.setStyleSheet("""
            #stockHeaderCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F0F9FF, stop:1 #EFF6FF);
                border-radius: 14px;
                border: 1px solid #E0F2FE;
            }
        """)

        stock_header_layout = QVBoxLayout(stock_header_card)
        stock_header_layout.setContentsMargins(20, 20, 20, 20)
        stock_header_layout.setSpacing(15)

        # Stock name and price
        stock_info = QVBoxLayout()

        self.stock_name = self._create_styled_label("", font_size=26, is_bold=True, color="#0F172A")

        price_layout = QHBoxLayout()
        self.stock_price = self._create_styled_label("", font_size=36, is_bold=True, color="#0F172A")

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

    def _create_stats_card(self):
        """Create the stock statistics card"""
        stats_card = QFrame()
        stats_card.setObjectName("statsCard")
        stats_card.setStyleSheet(
            "#statsCard {background-color: white; border-radius: 14px; border: 1px solid #E2E8F0;}")

        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        stats_layout.setSpacing(15)

        stats_title = self._create_styled_label("Stock Statistics", font_size=18, is_bold=True, color="#0F172A")

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(20)
        stats_grid.setVerticalSpacing(15)

        # Create statistics fields - these will be populated dynamically
        self.stats_fields = {
            "52_week_high": self._create_stat_field("52 Week High:", "", 0, 0),
            "beta": self._create_stat_field("Beta:", "", 0, 2),
            "52_week_low": self._create_stat_field("52 Week Low:", "", 1, 0),
            "pe_ratio": self._create_stat_field("P/E Ratio:", "", 1, 2),
            "avg_volume": self._create_stat_field("Avg Volume:", "", 2, 0),
            "dividend": self._create_stat_field("Dividend:", "", 2, 2)
        }

        for field_data in self.stats_fields.values():
            stats_grid.addWidget(field_data["label"], field_data["row"], field_data["col"])
            stats_grid.addWidget(field_data["value"], field_data["row"], field_data["col"] + 1)

        stats_layout.addWidget(stats_title)
        stats_layout.addLayout(stats_grid)

        return stats_card

    def _create_stat_field(self, label_text, value_text, row, col):
        """Create a statistics field with label and value"""
        label = QLabel(label_text)
        label.setStyleSheet("color: #64748B; font-size: 14px;")

        value = QLabel(value_text)
        value.setStyleSheet("color: #0F172A; font-weight: bold; font-size: 14px;")

        return {"label": label, "value": value, "row": row, "col": col}

    def _create_order_panel(self):
        """Create the order panel for buying/selling stocks"""
        order_panel = QFrame()
        order_panel.setObjectName("orderPanel")
        order_panel.setMinimumWidth(360)
        order_panel.setMaximumWidth(420)
        self._apply_shadow_effect(order_panel)
        order_panel.setStyleSheet("#orderPanel {background-color: white; border-radius: 16px; border: none;}")

        order_layout = QVBoxLayout(order_panel)
        order_layout.setContentsMargins(25, 25, 25, 25)
        order_layout.setSpacing(20)

        # Order header
        order_header = self._create_styled_label("Place Order", font_size=22, is_bold=True, color="#0F172A")

        # Order type
        order_type_label = self._create_styled_label("Order Type", font_size=15, is_bold=True, color="#334155")

        # Buy/Sell buttons
        order_type_buttons = QHBoxLayout()
        order_type_buttons.setSpacing(15)

        self.buy_button = self._create_toggle_button("Buy", "buyButton", True, is_buy=True)
        self.sell_button = self._create_toggle_button("Sell", "sellButton", False, is_buy=False)

        order_type_buttons.addWidget(self.buy_button)
        order_type_buttons.addWidget(self.sell_button)

        # Quantity
        quantity_label = self._create_styled_label("Quantity", font_size=15, is_bold=True, color="#334155")

        self.quantity_input = QLineEdit()
        self.quantity_input.setText("1")
        self.quantity_input.setValidator(QIntValidator(1, 10000))
        self.quantity_input.setMinimumHeight(45)
        self.quantity_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 15px;
                background-color: #F8FAFC;
                font-size: 15px;
                color: #1E293B;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
                background-color: white;
            }
        """)

        # Price info card
        price_info_card = self._create_price_info_card()

        # Buy/Sell action button
        self.action_button = QPushButton("")
        self.action_button.setObjectName("actionButton")
        self.action_button.setMinimumHeight(54)
        self.action_button.setCursor(Qt.PointingHandCursor)
        self._update_action_button(is_buy=True)

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
        price_info_card = QFrame()
        price_info_card.setObjectName("priceInfoCard")
        price_info_card.setStyleSheet("""
            #priceInfoCard {
                background-color: #F8FAFC;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)

        price_info_layout = QVBoxLayout(price_info_card)
        price_info_layout.setContentsMargins(15, 15, 15, 15)
        price_info_layout.setSpacing(10)

        price_grid = QGridLayout()
        price_grid.setHorizontalSpacing(10)
        price_grid.setVerticalSpacing(12)

        price_label = QLabel("Market Price:")
        price_label.setStyleSheet("color: #64748B; font-size: 15px;")

        self.price_value = QLabel("$0.00")
        self.price_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.price_value.setStyleSheet("font-weight: bold; color: #0F172A; font-size: 15px;")

        total_label = QLabel("Total Value:")
        total_label.setStyleSheet("color: #64748B; font-size: 15px;")

        self.total_value = QLabel("$0.00")
        self.total_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.total_value.setStyleSheet("font-weight: bold; color: #0F172A; font-size: 15px;")

        price_grid.addWidget(price_label, 0, 0)
        price_grid.addWidget(self.price_value, 0, 1)
        price_grid.addWidget(total_label, 1, 0)
        price_grid.addWidget(self.total_value, 1, 1)

        price_info_layout.addLayout(price_grid)

        return price_info_card

    def _create_styled_label(self, text, font_size=14, is_bold=False, color="#334155", margin_bottom=0):
        """Create a styled label with consistent formatting"""
        label = QLabel(text)

        bold_text = "font-weight: bold;" if is_bold else ""
        margin = f"margin-bottom: {margin_bottom}px;" if margin_bottom > 0 else ""

        label.setStyleSheet(f"""
            font-size: {font_size}px;
            {bold_text}
            color: {color};
            {margin}
        """)

        return label

    def _create_form_field(self, label_text, input_name, placeholder=""):
        """Create a form field with label and input"""
        layout = QVBoxLayout()

        label = self._create_styled_label(label_text, is_bold=True, font_size=14, margin_bottom=5)

        input_field = QLineEdit()
        setattr(self, input_name, input_field)
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(45)
        input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 15px;
                background-color: #F8FAFC;
                font-size: 15px;
                color: #1E293B;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
                background-color: white;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(input_field)

        return layout

    def _create_date_field(self, label_text, date_name, default_date):
        """Create a date field with label and date input"""
        layout = QVBoxLayout()

        label = self._create_styled_label(label_text, is_bold=True, font_size=14, margin_bottom=5)

        date_field = QDateEdit()
        setattr(self, date_name, date_field)
        date_field.setMinimumHeight(45)
        date_field.setCalendarPopup(True)
        date_field.setDisplayFormat("dd/MM/yyyy")
        date_field.setDate(default_date)
        date_field.setStyleSheet("""
            QDateEdit {
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px 15px;
                background-color: #F8FAFC;
                font-size: 15px;
                color: #1E293B;
            }
            QDateEdit:focus {
                border: 2px solid #3B82F6;
                background-color: white;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 25px;
                border: none;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(date_field)

        return layout

    def _create_primary_button(self, text, object_name):
        """Create a primary styled button"""
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setMinimumHeight(45)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            #{object_name} {{
                background-color: #3B82F6;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                padding: 10px 25px;
                font-size: 15px;
                border: none;
            }}
            #{object_name}:hover {{
                background-color: #2563EB;
            }}
            #{object_name}:pressed {{
                background-color: #1D4ED8;
            }}
        """)

        return button

    def _create_toggle_button(self, text, object_name, is_checked=False, is_buy=True):
        """Create a toggle button for buy/sell options"""
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setCheckable(True)
        button.setChecked(is_checked)
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(45)

        active_color = "#10B981" if is_buy else "#EF4444"

        button.setStyleSheet(f"""
            #{object_name} {{
                background-color: #F1F5F9;
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 15px;
                color: #334155;
            }}
            #{object_name}:checked {{
                background-color: {active_color};
                color: white;
                border: 2px solid {active_color};
            }}
            #{object_name}:hover:!checked {{
                background-color: #E2E8F0;
            }}
        """)

        return button

    def _apply_shadow_effect(self, widget):
        """Apply a shadow effect to a widget"""
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(15, 23, 42, 40))
        shadow_effect.setOffset(0, 4)
        widget.setGraphicsEffect(shadow_effect)

    def _update_action_button(self, is_buy=True, symbol=""):
        """Update the action button style and text based on buy/sell status"""
        action_text = f"{'Buy' if is_buy else 'Sell'} {symbol}" if symbol else f"{'Buy' if is_buy else 'Sell'}"
        self.action_button.setText(action_text)

        button_color = "#10B981" if is_buy else "#EF4444"
        hover_color = "#059669" if is_buy else "#DC2626"
        pressed_color = "#047857" if is_buy else "#B91C1C"

        self.action_button.setStyleSheet(f"""
            #actionButton {{
                background-color: {button_color};
                color: white;
                border-radius: 12px;
                font-weight: bold;
                padding: 12px;
                font-size: 16px;
                border: none;
            }}
            #actionButton:hover {{
                background-color: {hover_color};
            }}
            #actionButton:pressed {{
                background-color: {pressed_color};
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

    def update_stock_data(self, stock_data):
        """Update stock information in the UI

        Args:
            stock_data (dict): Dictionary containing stock information with keys:
                - name: Company name
                - symbol: Stock symbol
                - price: Current price
                - change_pct: Percentage change
                - volume: Trading volume
                - market_cap: Market capitalization in billions
                - stats: Dictionary with statistics (52_week_high, 52_week_low, etc.)
        """
        # Update stock header
        self.stock_name.setText(f"{stock_data['name']} ({stock_data['symbol']})")
        self.stock_price.setText(f"${stock_data['price']:.2f}")

        # Format change percentage with color
        if stock_data['change_pct'] >= 0:
            self.stock_change.setText(f"{stock_data['change_pct']:.1f}%")
            self.stock_change.setStyleSheet("""
                color: #10B981; 
                font-weight: bold;
                font-size: 18px;
                background-color: #ECFDF5;
                border-radius: 8px;
                padding: 5px 10px;
                margin-left: 10px;
            """)
        else:
            self.stock_change.setText(f"{stock_data['change_pct']:.1f}%")
            self.stock_change.setStyleSheet("""
                color: #EF4444; 
                font-weight: bold;
                font-size: 18px;
                background-color: #FEF2F2;
                border-radius: 8px;
                padding: 5px 10px;
                margin-left: 10px;
            """)

        # Format volume with commas
        formatted_volume = f"{stock_data['volume']:,}"
        self.volume_label.setText(f"Volume: {formatted_volume}")

        # Format market cap
        if stock_data['market_cap'] >= 1000:
            self.market_cap_label.setText(f"Market Cap: ${stock_data['market_cap'] / 1000:.2f}T")
        else:
            self.market_cap_label.setText(f"Market Cap: ${stock_data['market_cap']:.2f}B")

        # Update order panel
        self.price_value.setText(f"${stock_data['price']:.2f}")
        self.update_total_value()

        # Update action button text
        is_buy = self.buy_button.isChecked()
        self._update_action_button(is_buy=is_buy, symbol=stock_data['symbol'])

        # Update statistics if provided
        if 'stats' in stock_data:
            stats = stock_data['stats']

            # Update each stat field with proper formatting
            for key, value in stats.items():
                if key in self.stats_fields:
                    if key in ['52_week_high', '52_week_low']:
                        self.stats_fields[key]['value'].setText(f"${value:.2f}")
                    elif key == 'avg_volume':
                        self.stats_fields[key]['value'].setText(f"{value:,}")
                    elif key == 'dividend':
                        self.stats_fields[key]['value'].setText(f"{value:.2f}%")
                    else:
                        self.stats_fields[key]['value'].setText(f"{value}")

        # Update chart with provided stock data
        if 'chart_data' in stock_data:
            self.chart.update_chart(stock_data['chart_data'])



    def show_message(self, message, is_error=False):
        """Display a message to the user"""
        # This could be implemented with a popup dialog, status bar, or in-app notification
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


class MainWindow(QMainWindow):
    """Main window for the stock trading application"""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
        self.load_demo_data()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Modern Stock Trading App")
        self.resize(1200, 900)

        # Set application icon
        # self.setWindowIcon(QIcon("icon.png"))

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create stock trading view
        self.stock_view = StockTradingView()
        main_layout.addWidget(self.stock_view)

    def setup_connections(self):
        """Set up signal connections"""
        self.stock_view.search_stock_requested.connect(self.on_search_stock)
        self.stock_view.buy_stock_requested.connect(self.on_buy_stock)
        self.stock_view.sell_stock_requested.connect(self.on_sell_stock)

    def on_search_stock(self, symbol, start_date, end_date):
        """Handle stock search request"""
        print(f"Searching for {symbol} from {start_date.toString('yyyy-MM-dd')} to {end_date.toString('yyyy-MM-dd')}")

        # In a real app, you would fetch data from an API
        # For demo purposes, we'll use sample data
        self.load_demo_data(symbol)

    def on_buy_stock(self, symbol, quantity, price):
        """Handle buy stock request"""
        total = quantity * price
        print(f"Buying {quantity} shares of {symbol} at ${price:.2f} for a total of ${total:.2f}")
        # In a real app, you would send this to a trading API

    def on_sell_stock(self, symbol, quantity, price):
        """Handle sell stock request"""
        total = quantity * price
        print(f"Selling {quantity} shares of {symbol} at ${price:.2f} for a total of ${total:.2f}")
        # In a real app, you would send this to a trading API

    def load_demo_data(self, symbol=None):
        """Load demo data for display"""
        if not symbol:
            symbol = "AAPL"

        # Sample data for demonstration
        sample_data = {
            "AAPL": {
                "name": "Apple Inc.",
                "symbol": "AAPL",
                "price": 190.47,
                "change_pct": 2.4,
                "volume": 74250000,
                "market_cap": 2970.5,
                "stats": {
                    "52_week_high": 199.62,
                    "52_week_low": 149.35,
                    "avg_volume": 59840000,
                    "pe_ratio": 29.3,
                    "beta": 1.28,
                    "dividend": 0.58
                },
                "chart_data": {}  # This would contain price points for the chart
            },
            "MSFT": {
                "name": "Microsoft Corporation",
                "symbol": "MSFT",
                "price": 334.51,
                "change_pct": -0.8,
                "volume": 22140000,
                "market_cap": 2486.3,
                "stats": {
                    "52_week_high": 366.78,
                    "52_week_low": 310.24,
                    "avg_volume": 27520000,
                    "pe_ratio": 31.2,
                    "beta": 0.92,
                    "dividend": 0.95
                },
                "chart_data": {}
            },
            "GOOGL": {
                "name": "Alphabet Inc.",
                "symbol": "GOOGL",
                "price": 145.72,
                "change_pct": 1.3,
                "volume": 31250000,
                "market_cap": 1820.4,
                "stats": {
                    "52_week_high": 153.78,
                    "52_week_low": 121.55,
                    "avg_volume": 22680000,
                    "pe_ratio": 25.1,
                    "beta": 1.05,
                    "dividend": 0.0
                },
                "chart_data": {}
            }
        }

        # Use the requested symbol or fallback to default
        stock_data = sample_data.get(symbol, sample_data["AAPL"])

        # Update the view with the stock data
        self.stock_view.update_stock_data(stock_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
