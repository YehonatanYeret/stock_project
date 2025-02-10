# File: views/main_view.py
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, 
                               QHBoxLayout, QPushButton)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QIcon

from Views.home_page import HomePage
from Views.portfolio_page import PortfolioPage
from Views.stock_search_page import StockSearchPage

class MainView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Navigation Layout
        nav_layout = QHBoxLayout()
        
        # Navigation Buttons
        self.home_btn = self.create_nav_button("Home", "home_icon.png")
        self.portfolio_btn = self.create_nav_button("Portfolio", "portfolio_icon.png")
        self.search_btn = self.create_nav_button("Search", "search_icon.png")
        
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.portfolio_btn)
        nav_layout.addWidget(self.search_btn)
        
        # Stacked Widget for Pages
        self.stacked_widget = QStackedWidget()
        
        # Create Pages
        self.home_page = HomePage()
        self.portfolio_page = PortfolioPage()
        self.stock_search_page = StockSearchPage()
        
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.portfolio_page)
        self.stacked_widget.addWidget(self.stock_search_page)
        
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stacked_widget)

    def create_nav_button(self, text, icon_path):
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3c3f41;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a4d4f;
            }
        """)
        return btn

    def slide_to_page(self, page_index):
        """Slide animation between pages"""
        current_index = self.stacked_widget.currentIndex()
        if current_index == page_index:
            return

        current_widget = self.stacked_widget.currentWidget()
        next_widget = self.stacked_widget.widget(page_index)

        # Determine slide direction
        direction = 1 if page_index > current_index else -1

        # Set initial positions
        current_widget.setGeometry(0, 0, current_widget.width(), current_widget.height())
        next_widget.setGeometry(
            direction * current_widget.width(), 
            0, 
            next_widget.width(), 
            next_widget.height()
        )

        # Animations
        current_anim = QPropertyAnimation(current_widget, b"pos")
        current_anim.setDuration(300)
        current_anim.setStartValue(QPoint(0, 0))
        current_anim.setEndValue(QPoint(-direction * current_widget.width(), 0))
        current_anim.setEasingCurve(QEasingCurve.InOutQuad)

        next_anim = QPropertyAnimation(next_widget, b"pos")
        next_anim.setDuration(300)
        next_anim.setStartValue(QPoint(direction * current_widget.width(), 0))
        next_anim.setEndValue(QPoint(0, 0))
        next_anim.setEasingCurve(QEasingCurve.InOutQuad)

        current_anim.start()
        next_anim.start()

        self.stacked_widget.setCurrentIndex(page_index)