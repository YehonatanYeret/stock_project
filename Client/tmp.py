import sys
import random
from datetime import datetime, timedelta
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QDateEdit, QFrame, 
    QStackedWidget, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QDate, QPointF, QMargins, QSize
from PySide6.QtGui import QIcon, QColor, QPen, QFont, QPixmap, QPainter, QPainterPath, QLinearGradient, QGradient
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QAreaSeries

class IconButton(QPushButton):
    def __init__(self, icon_path=None, color="#5851DB", parent=None):
        super().__init__(parent)
        self.setFlat(True)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {color};
                font-size: 18px;
                padding: 8px;
            }}
            QPushButton:hover {{
                background-color: rgba(88, 81, 219, 0.1);
                border-radius: 4px;
            }}
        """)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))

class StockPerformanceChart(QWidget):
    def __init__(self, parent=None, data=None, min_y=None, max_y=None, title="Stock Performance"):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create chart
        self.chart = QChart()
        self.chart.setTitle(title)
        self.chart.setTitleFont(QFont("Arial", 16))
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(10, 10, 10, 10))
        self.chart.setContentsMargins(10, 10, 10, 10)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeLight)
        self.chart.setDropShadowEnabled(True)
        
        # Create line series
        self.series = QLineSeries()
        self.series.setPen(QPen(QColor("#4C6FFF"), 3))
        
        # Create area series for shaded area under curve
        self.area_series = QAreaSeries(self.series)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(76, 111, 255, 150))
        gradient.setColorAt(1.0, QColor(76, 111, 255, 20))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        self.area_series.setBrush(gradient)
        self.area_series.setPen(Qt.NoPen)
        
        # Add data to series
        if data is None:
            data = self.generate_random_data()
        
        for i, value in enumerate(data):
            self.series.append(QPointF(i, value))
        
        self.chart.addSeries(self.area_series)
        self.chart.addSeries(self.series)
        
        # Create X axis
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, len(data) - 1)
        self.axis_x.setLabelsVisible(False)
        self.axis_x.setGridLineVisible(True)
        self.axis_x.setGridLineColor(QColor("#E5E5E5"))
        self.axis_x.setTickCount(10)
        self.axis_x.setLinePenColor(QColor("#CCCCCC"))
        
        # Create Y axis
        self.axis_y = QValueAxis()
        if min_y is not None and max_y is not None:
            self.axis_y.setRange(min_y, max_y)
        else:
            self.axis_y.setRange(min(data) * 0.9, max(data) * 1.1)
        self.axis_y.setLabelsVisible(True)
        self.axis_y.setGridLineVisible(True)
        self.axis_y.setGridLineColor(QColor("#E5E5E5"))
        self.axis_y.setTickCount(6)
        self.axis_y.setLinePenColor(QColor("#CCCCCC"))
        self.axis_y.setLabelFormat("%.0f")
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        self.area_series.attachAxis(self.axis_x)
        self.area_series.attachAxis(self.axis_y)
        
        # Create chart view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(300)
        
        # Add padding around the chart
        chart_container = QFrame()
        chart_container.setObjectName("chartContainer")
        chart_container.setStyleSheet("""
            #chartContainer {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #EAEAEA;
            }
        """)
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(10, 20, 10, 10)
        chart_layout.addWidget(self.chart_view)
        
        self.layout.addWidget(chart_container)
    
    def generate_random_data(self, n_points=30):
        # Generate data that resembles stock prices
        base = 200
        volatility = 30
        data = [base]
        
        for _ in range(n_points - 1):
            change = random.uniform(-1, 1) * volatility
            new_value = max(50, data[-1] + change)
            data.append(new_value)
        
        return data

class StatCard(QFrame):
    def __init__(self, title, value, subtitle=None, icon=None, color="#5851DB", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setStyleSheet("""
            #StatCard {
                background-color: white;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
                border: 1px solid #EAEAEA;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        
        # Header with title and icon
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
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: #000; font-size: 28px; font-weight: bold;")
        self.layout.addWidget(value_label)
        
        # Subtitle (optional)
        if subtitle:
            subtitle_layout = QHBoxLayout()
            
            # Create arrow icon based on positive/negative value
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

class StockFolioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StockFolio")
        self.resize(1100, 800)
        
        # Set app style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8FAFF;
            }
            QLabel {
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QLineEdit, QDateEdit {
                padding: 12px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 2px solid #4C6FFF;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create main content area
        content_container = QFrame()
        content_container.setStyleSheet("""
            background-color: #F8FAFF;
            border-top-left-radius: 20px;
            margin-left: 0px;
        """)
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked pages
        self.content_stack = QStackedWidget()
        
        # Pages
        self.search_page = self.create_search_page()
        self.dashboard_page = self.create_dashboard_page()
        self.trade_page = self.create_trade_page()  # NEW TRADE PAGE
        
        self.content_stack.addWidget(self.search_page)
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.trade_page)
        
        content_layout.addWidget(self.content_stack)
        main_layout.addWidget(content_container, 1)
        
        # Connect buttons
        self.connect_buttons()
        
        # Show dashboard by default
        self.content_stack.setCurrentIndex(1)
    
    def create_sidebar(self):
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            background-color: #FFFFFF;
            border-right: 1px solid #EAEAEA;
            padding: 0px;
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(28, 28, 28, 28)
        sidebar_layout.setSpacing(6)
        
        # Logo
        logo_layout = QHBoxLayout()
        logo_frame = QFrame()
        logo_frame.setFixedSize(40, 40)
        logo_frame.setStyleSheet("""
            background-color: #4C6FFF;
            border-radius: 8px;
        """)
        
        logo_inner_layout = QVBoxLayout(logo_frame)
        logo_inner_layout.setContentsMargins(0, 0, 0, 0)
        logo_inner_layout.setAlignment(Qt.AlignCenter)
        
        logo_icon = QLabel("$")
        logo_icon.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        logo_inner_layout.addWidget(logo_icon)
        
        logo_text = QLabel("StockFolio")
        logo_text.setStyleSheet("""
            color: #202020;
            font-size: 20px;
            font-weight: bold;
            margin-left: 10px;
        """)
        
        logo_layout.addWidget(logo_frame)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        sidebar_layout.addLayout(logo_layout)
        
        sidebar_layout.addSpacing(40)
        
        # Navigation buttons
        nav_style = """
            text-align: left;
            padding: 14px 20px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 4px;
        """
        
        self.active_style = nav_style + """
            background-color: #EEF2FF;
            color: #4C6FFF;
        """
        
        self.inactive_style = nav_style + """
            background-color: transparent;
            color: #666;
        """
        
        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setIcon(QIcon.fromTheme("go-home"))
        self.dashboard_btn.setStyleSheet(self.active_style)
        
        self.trade_btn = QPushButton("Trade")
        self.trade_btn.setIcon(QIcon.fromTheme("office-chart-bar"))
        self.trade_btn.setStyleSheet(self.inactive_style)
        
        self.history_btn = QPushButton("History")
        self.history_btn.setIcon(QIcon.fromTheme("document-open-recent"))
        self.history_btn.setStyleSheet(self.inactive_style)
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setIcon(QIcon.fromTheme("edit-find"))
        self.search_btn.setStyleSheet(self.inactive_style)
        
        self.ai_assistant_btn = QPushButton("AI Assistant")
        self.ai_assistant_btn.setIcon(QIcon.fromTheme("system-help"))
        self.ai_assistant_btn.setStyleSheet(self.inactive_style)
        
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setIcon(QIcon.fromTheme("preferences-system"))
        self.settings_btn.setStyleSheet(self.inactive_style)
        
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.trade_btn)
        sidebar_layout.addWidget(self.history_btn)
        sidebar_layout.addWidget(self.search_btn)
        sidebar_layout.addWidget(self.ai_assistant_btn)
        sidebar_layout.addWidget(self.settings_btn)
        
        sidebar_layout.addStretch(1)
        
        # Action buttons (bell/theme)
        header_actions = QHBoxLayout()
        bell_btn = QPushButton()
        bell_btn.setIcon(QIcon.fromTheme("preferences-desktop-notification"))
        bell_btn.setFixedSize(40, 40)
        bell_btn.setStyleSheet("""
            background-color: white;
            border: 1px solid #EAEAEA;
            border-radius: 8px;
        """)
        
        theme_btn = QPushButton()
        theme_btn.setIcon(QIcon.fromTheme("weather-clear-night"))
        theme_btn.setFixedSize(40, 40)
        theme_btn.setStyleSheet("""
            background-color: white;
            border: 1px solid #EAEAEA;
            border-radius: 8px;
        """)
        
        header_actions.addWidget(bell_btn)
        header_actions.addWidget(theme_btn)
        header_actions.addStretch()
        
        return sidebar
    
    def create_search_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header section
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)
        
        # Stock Symbol Input
        symbol_layout = QVBoxLayout()
        symbol_label = QLabel("Stock Symbol")
        symbol_label.setStyleSheet("font-size: 15px; font-weight: 500; margin-bottom: 8px;")
        symbol_input = QLineEdit()
        symbol_input.setPlaceholderText("Enter stock symbol")
        symbol_input.setMinimumHeight(50)
        symbol_layout.addWidget(symbol_label)
        symbol_layout.addWidget(symbol_input)
        
        # Start Date Input
        start_date_layout = QVBoxLayout()
        start_date_label = QLabel("Start Date")
        start_date_label.setStyleSheet("font-size: 15px; font-weight: 500; margin-bottom: 8px;")
        start_date_input = QDateEdit()
        start_date_input.setCalendarPopup(True)
        start_date_input.setDate(QDate(2024, 1, 1))
        start_date_input.setMinimumHeight(50)
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(start_date_input)
        
        # End Date Input
        end_date_layout = QVBoxLayout()
        end_date_label = QLabel("End Date")
        end_date_label.setStyleSheet("font-size: 15px; font-weight: 500; margin-bottom: 8px;")
        end_date_input = QDateEdit()
        end_date_input.setCalendarPopup(True)
        end_date_input.setDate(QDate(2024, 1, 31))
        end_date_input.setMinimumHeight(50)
        end_date_layout.addWidget(end_date_label)
        end_date_layout.addWidget(end_date_input)
        
        header_layout.addLayout(symbol_layout, 2)
        header_layout.addLayout(start_date_layout, 1)
        header_layout.addLayout(end_date_layout, 1)
        
        layout.addLayout(header_layout)
        layout.addSpacing(30)
        
        # Search Button
        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("""
            background-color: #4C6FFF;
            color: white;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            max-width: 150px;
        """)
        search_btn.setMinimumHeight(50)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(search_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        layout.addSpacing(40)
        
        # Chart Title
        chart_title = QLabel("Stock Performance")
        chart_title.setStyleSheet("font-size: 20px; font-weight: 600; color: #202020; margin-bottom: 10px;")
        layout.addWidget(chart_title)
        
        # Stock Chart
        stock_data = [160, 170, 240, 240, 200, 250, 230, 240, 180, 170, 170, 170, 200, 180, 200, 160, 200, 220, 200, 230, 210, 170, 200]
        stock_chart = StockPerformanceChart(data=stock_data, min_y=65, max_y=260)
        layout.addWidget(stock_chart)
        
        return page
    
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet("font-size: 26px; font-weight: 700; color: #202020; margin-bottom: 20px;")
        layout.addWidget(header)
        
        # Stats Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        portfolio_value = StatCard(
            "Portfolio Value", 
            "$125,430.50", 
            "+2.5% today", 
            None, 
            "#4CAF50"
        )
        
        total_stocks = StatCard(
            "Total Stocks", 
            "15", 
            "Across 8 companies", 
            None, 
            "#2196F3"
        )
        
        days_gain = StatCard(
            "Day's Gain", 
            "$3,125.40", 
            "+2.8%", 
            None, 
            "#4CAF50"
        )
        
        total_return = StatCard(
            "Total Return", 
            "$25,430.50", 
            "+15.4% all time", 
            None, 
            "#9C27B0"
        )
        
        stats_layout.addWidget(portfolio_value)
        stats_layout.addWidget(total_stocks)
        stats_layout.addWidget(days_gain)
        stats_layout.addWidget(total_return)
        
        layout.addLayout(stats_layout)
        layout.addSpacing(40)
        
        # Portfolio Title
        portfolio_title = QLabel("Portfolio Performance")
        portfolio_title.setStyleSheet("font-size: 20px; font-weight: 600; color: #202020; margin-bottom: 10px;")
        layout.addWidget(portfolio_title)
        
        # Portfolio Performance Chart
        portfolio_data = self.generate_portfolio_data()
        portfolio_chart = StockPerformanceChart(
            data=portfolio_data, 
            title="Portfolio Performance",
            min_y=1500,
            max_y=6000
        )
        layout.addWidget(portfolio_chart)
        
        return page

    def create_trade_page(self):
        """
        Creates a 'Trade' page matching the style in your screenshot:
        - Stock Symbol, Date inputs, Search button
        - Stock info + chart on the left
        - Place Order card on the right
        """
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # --- Top row (symbol + dates + search) ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)

        # Symbol
        symbol_layout = QVBoxLayout()
        sym_label = QLabel("Stock Symbol")
        sym_label.setStyleSheet("font-size: 15px; font-weight: 500; margin-bottom: 8px;")
        sym_input = QLineEdit("AAPL")
        sym_input.setMinimumHeight(45)
        symbol_layout.addWidget(sym_label)
        symbol_layout.addWidget(sym_input)

        # Start date
        start_layout = QVBoxLayout()
        start_label = QLabel("Start Date")
        start_label.setStyleSheet("font-size: 15px; font-weight: 500; margin-bottom: 8px;")
        start_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDate(QDate(2024, 1, 1))
        start_date.setMinimumHeight(45)
        start_layout.addWidget(start_label)
        start_layout.addWidget(start_date)

        # End date
        end_layout = QVBoxLayout()
        end_label = QLabel("End Date")
        end_label.setStyleSheet("font-size: 15px; font-weight: 500; margin-bottom: 8px;")
        end_date = QDateEdit()
        end_date.setCalendarPopup(True)
        end_date.setDate(QDate(2024, 1, 31))
        end_date.setMinimumHeight(45)
        end_layout.addWidget(end_label)
        end_layout.addWidget(end_date)

        # Search button
        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("""
            background-color: #4C6FFF;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            max-width: 120px;
        """)
        search_btn.setMinimumHeight(45)

        top_layout.addLayout(symbol_layout, 2)
        top_layout.addLayout(start_layout, 1)
        top_layout.addLayout(end_layout, 1)
        top_layout.addWidget(search_btn)

        main_layout.addLayout(top_layout)
        main_layout.addSpacing(30)

        # --- Middle row: Stock info & chart on the left, Order form on the right ---
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(20)

        # Left: Stock Info + Chart
        left_container = QVBoxLayout()

        # Stock info block
        stock_info_frame = QFrame()
        stock_info_frame.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            border: 1px solid #EAEAEA;
        """)
        stock_info_layout = QVBoxLayout(stock_info_frame)
        stock_info_layout.setContentsMargins(20, 20, 20, 20)

        stock_title = QLabel("Apple Inc. (AAPL)")
        stock_title.setStyleSheet("font-size: 20px; font-weight: 600; color: #202020;")
        stock_price = QLabel("$175.25  ")
        stock_price.setStyleSheet("font-size: 18px; font-weight: 600; color: #00BFA6;")  # greenish
        sub_info = QLabel("Volume: 55,000,000   |   Market Cap: $2800.00B")
        sub_info.setStyleSheet("color: #777; font-size: 14px;")

        stock_info_layout.addWidget(stock_title)
        stock_info_layout.addWidget(stock_price)
        stock_info_layout.addWidget(sub_info)

        left_container.addWidget(stock_info_frame)
        left_container.addSpacing(10)

        # Chart
        chart_data = [160, 170, 240, 240, 200, 250, 230, 240, 180, 170, 170, 170, 
                      200, 180, 200, 160, 200, 220, 200, 230, 210, 170, 200]
        stock_chart = StockPerformanceChart(data=chart_data, min_y=65, max_y=260)
        left_container.addWidget(stock_chart)

        # Right: Place Order
        order_frame = QFrame()
        order_frame.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            border: 1px solid #EAEAEA;
        """)
        order_layout = QVBoxLayout(order_frame)
        order_layout.setContentsMargins(20, 20, 20, 20)
        order_layout.setSpacing(15)

        order_title = QLabel("Place Order")
        order_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #202020;")
        order_layout.addWidget(order_title)

        # Order type
        type_layout = QHBoxLayout()
        buy_btn = QPushButton("Buy")
        buy_btn.setStyleSheet("""
            background-color: #28a745; 
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
        """)
        sell_btn = QPushButton("Sell")
        sell_btn.setStyleSheet("""
            background-color: #E0E0E0; 
            color: #333;
            border-radius: 6px;
            padding: 10px 20px;
        """)
        type_layout.addWidget(buy_btn)
        type_layout.addWidget(sell_btn)
        order_layout.addLayout(type_layout)

        # Quantity
        qty_label = QLabel("Quantity")
        qty_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #333;")
        order_layout.addWidget(qty_label)

        qty_input = QLineEdit("1")
        qty_input.setStyleSheet("padding: 10px; border: 1px solid #CCC; border-radius: 6px;")
        order_layout.addWidget(qty_input)

        # Price info
        market_label = QLabel("Market Price:  $175.25")
        market_label.setStyleSheet("color: #777; font-size: 14px;")
        total_label = QLabel("Total Value:  $175.25")
        total_label.setStyleSheet("color: #777; font-size: 14px;")

        order_layout.addWidget(market_label)
        order_layout.addWidget(total_label)

        # Big buy button
        final_buy_btn = QPushButton("Buy AAPL")
        final_buy_btn.setStyleSheet("""
            background-color: #28a745; 
            color: white;
            font-size: 16px;
            font-weight: 600;
            padding: 12px 0px;
            border-radius: 6px;
        """)
        order_layout.addWidget(final_buy_btn)

        middle_layout.addLayout(left_container, 2)
        middle_layout.addWidget(order_frame, 1)

        main_layout.addLayout(middle_layout)

        return page
    
    def generate_portfolio_data(self, n_points=20):
        # Generate portfolio performance data with an upward trend
        data = [4000]
        
        # Initial downward trend
        for i in range(5):
            change = random.uniform(-0.05, -0.01) * data[-1]
            data.append(data[-1] + change)
        
        # Recovery and growth
        for i in range(14):
            if i < 7:
                change = random.uniform(0.02, 0.07) * data[-1]
            else:
                change = random.uniform(-0.01, 0.05) * data[-1]
            data.append(data[-1] + change)
        
        return data
    
    def connect_buttons(self):
        # Connect sidebar buttons to switch pages
        self.dashboard_btn.clicked.connect(self._show_dashboard)
        self.search_btn.clicked.connect(self._show_search)
        self.trade_btn.clicked.connect(self._show_trade)

    # -- Page switching logic with style updates --
    def _show_dashboard(self):
        self.content_stack.setCurrentIndex(1)
        self.dashboard_btn.setStyleSheet(self.active_style)
        self.trade_btn.setStyleSheet(self.inactive_style)
        self.history_btn.setStyleSheet(self.inactive_style)
        self.search_btn.setStyleSheet(self.inactive_style)
        self.ai_assistant_btn.setStyleSheet(self.inactive_style)
        self.settings_btn.setStyleSheet(self.inactive_style)
    
    def _show_search(self):
        self.content_stack.setCurrentIndex(0)
        self.search_btn.setStyleSheet(self.active_style)
        self.dashboard_btn.setStyleSheet(self.inactive_style)
        self.trade_btn.setStyleSheet(self.inactive_style)
        self.history_btn.setStyleSheet(self.inactive_style)
        self.ai_assistant_btn.setStyleSheet(self.inactive_style)
        self.settings_btn.setStyleSheet(self.inactive_style)

    def _show_trade(self):
        # Switch to Trade Page
        self.content_stack.setCurrentIndex(2)
        self.trade_btn.setStyleSheet(self.active_style)
        self.dashboard_btn.setStyleSheet(self.inactive_style)
        self.history_btn.setStyleSheet(self.inactive_style)
        self.search_btn.setStyleSheet(self.inactive_style)
        self.ai_assistant_btn.setStyleSheet(self.inactive_style)
        self.settings_btn.setStyleSheet(self.inactive_style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockFolioApp()
    window.show()
    sys.exit(app.exec())
