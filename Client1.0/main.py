from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from views.auth_views import AuthStackedWidget
from views.components.icon_button import IconButton

class SidebarButton(QPushButton):
    """Styled button for sidebar navigation"""
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFlat(True)
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                color: #555555;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(76, 111, 255, 0.1);
                color: #4C6FFF;
            }
            QPushButton:checked {
                background-color: rgba(76, 111, 255, 0.2);
                color: #4C6FFF;
            }
        """)

class Sidebar(QFrame):
    """Application sidebar for navigation"""
    dashboard_clicked = Signal()
    portfolio_clicked = Signal()
    stocks_clicked = Signal()
    transactions_clicked = Signal()
    settings_clicked = Signal()
    logout_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setStyleSheet("""
            #sidebar {
                background-color: white;
                border-right: 1px solid #EAEAEA;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 20, 16, 20)
        self.layout.setSpacing(8)
        
        # Logo
        self.logo_label = QLabel("📈 STOCK PORTFOLIO")
        self.logo_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #4C6FFF;
                padding: 10px 0;
            }
        """)
        self.layout.addWidget(self.logo_label)
        
        # Navigation buttons
        self.dashboard_button = SidebarButton("Dashboard", "icons/dashboard.png")
        self.dashboard_button.setChecked(True)
        self.dashboard_button.clicked.connect(self.dashboard_clicked)
        self.layout.addWidget(self.dashboard_button)
        
        self.portfolio_button = SidebarButton("Portfolio", "icons/portfolio.png")
        self.portfolio_button.clicked.connect(self.portfolio_clicked)
        self.layout.addWidget(self.portfolio_button)
        
        self.stocks_button = SidebarButton("Stocks", "icons/stocks.png")
        self.stocks_button.clicked.connect(self.stocks_clicked)
        self.layout.addWidget(self.stocks_button)
        
        self.transactions_button = SidebarButton("Transactions", "icons/transactions.png")
        self.transactions_button.clicked.connect(self.transactions_clicked)
        self.layout.addWidget(self.transactions_button)
        
        self.settings_button = SidebarButton("Settings", "icons/settings.png")
        self.settings_button.clicked.connect(self.settings_clicked)
        self.layout.addWidget(self.settings_button)
        
        # Add spacer to push logout to bottom
        self.layout.addStretch()
        
        # Logout button
        self.logout_button = SidebarButton("Logout", "icons/logout.png")
        self.logout_button.clicked.connect(self.logout_clicked)
        self.layout.addWidget(self.logout_button)
        
        # Set fixed width
        self.setMinimumWidth(220)
        self.setMaximumWidth(220)
    
    def set_active_button(self, button_name):
        """Set the active button in the sidebar"""
        buttons = {
            "dashboard": self.dashboard_button,
            "portfolio": self.portfolio_button,
            "stocks": self.stocks_button,
            "transactions": self.transactions_button,
            "settings": self.settings_button
        }
        
        for name, button in buttons.items():
            button.setChecked(name == button_name)

class MainWindow(QMainWindow):
    """Main application window"""
    # Authentication signals
    login_requested = Signal(str, str)
    register_requested = Signal(str, str, str)
    logout_requested = Signal()
    
    # Navigation signals
    dashboard_requested = Signal()
    portfolio_requested = Signal()
    stocks_requested = Signal()
    transactions_requested = Signal()
    settings_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Portfolio Manager")
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create authentication stack
        self.auth_stack = AuthStackedWidget()
        self.auth_stack.login_requested.connect(self.login_requested)
        self.auth_stack.register_requested.connect(self.register_requested)
        
        # Create sidebar
        self.sidebar = Sidebar()
        self.sidebar.dashboard_clicked.connect(self.dashboard_requested)
        self.sidebar.portfolio_clicked.connect(self.portfolio_requested)
        self.sidebar.stocks_clicked.connect(self.stocks_requested)
        self.sidebar.transactions_clicked.connect(self.transactions_requested)
        self.sidebar.settings_clicked.connect(self.settings_requested)
        self.sidebar.logout_clicked.connect(self.logout_requested)
        
        # Create content stack
        self.content_stack = QStackedWidget()
        
        # Create placeholder content (will be replaced later)
        self.dashboard_widget = QWidget()
        self.portfolio_widget = QWidget()
        self.stocks_widget = QWidget()
        self.transactions_widget = QWidget()
        self.settings_widget = QWidget()
        
        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.portfolio_widget)
        self.content_stack.addWidget(self.stocks_widget)
        self.content_stack.addWidget(self.transactions_widget)
        self.content_stack.addWidget(self.settings_widget)
        
        # Main application layout (sidebar + content)
        self.app_layout = QHBoxLayout()
        self.app_layout.setContentsMargins(0, 0, 0, 0)
        self.app_layout.setSpacing(0)
        self.app_layout.addWidget(self.sidebar)
        self.app_layout.addWidget(self.content_stack)
        
        # Main application widget
        self.app_widget = QWidget()
        self.app_widget.setLayout(self.app_layout)
        
        # Main stacked widget to switch between auth and app
        self.main_stack = QStackedWidget()
        self.main_stack.addWidget(self.auth_stack)
        self.main_stack.addWidget(self.app_widget)
        
        # Add main stack to main layout
        self.main_layout.addWidget(self.main_stack)
        
        # Start with auth screen
        self.show_auth()
        
        # Set window size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F9FA;
            }
        """)
    
    def show_auth(self):
        """Show the authentication screen"""
        self.main_stack.setCurrentWidget(self.auth_stack)
    
    def show_app(self):
        """Show the main application screen"""
        self.main_stack.setCurrentWidget(self.app_widget)