from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from views.mainViews.dashboard_view import DashboardView
from presenters.mainPresenters.dashboard_presenter import DashboardPresenter
from models.mainModels.dashboard_model import DashboardModel
from views.mainViews.stock_view import StockView
from presenters.mainPresenters.stock_presenter import StockPresenter
from models.mainModels.stock_model import StockModel
# from views.mainViews.history_view import HistoryView
# from presenters.mainPresenters.history_presenter import HistoryPresenter
# from models.mainModels.history_model import HistoryModel



class SidebarButton(QPushButton):
    """Styled button for sidebar navigation with exclusive selection."""

    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFlat(True)

        if icon_path:
            self.setIcon(QIcon(icon_path))

        self.set_default_style()

    def set_default_style(self):
        """Set the default unselected button style."""
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
        """)

    def set_active(self, is_active):
        """Set button as active or inactive."""
        if is_active:
            self.setStyleSheet("""
                QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                background-color: rgba(76, 111, 255, 0.2);
                color: #4C6FFF;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(76, 111, 255, 0.1);
                color: #4C6FFF;
            }
            """)
            self.setChecked(True)
        else:
            self.set_default_style()
            self.setChecked(False)


class Sidebar(QFrame):
    """Application sidebar for navigation with exclusive selection."""

    dashboard_clicked = Signal()
    stock_clicked = Signal()
    history_clicked = Signal()
    chatbot_clicked = Signal()
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
        self.logo_label = self.logo_label = QLabel("📈 STOCK PORTFOLIO")
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
        self.buttons = {}

        self.dashboard_button = self.create_sidebar_button("Dashboard", "icons/dashboard.png", self.dashboard_clicked)
        self.stocks_button = self.create_sidebar_button("Stocks", "icons/trade.png", self.stock_clicked)
        self.history_button = self.create_sidebar_button("History", "icons/history.png", self.history_clicked)
        self.chatbot_button = self.create_sidebar_button("Chatbot", "icons/chatbot.png", self.chatbot_clicked)
        self.settings_button = self.create_sidebar_button("Settings", "icons/settings.png", self.settings_clicked)

        self.layout.addStretch()

        # Add spacer to push logout to bottom
        self.logout_button = self.create_sidebar_button("Logout", "icons/logout.png", self.logout_clicked, logout=True)

        # Set fixed width
        self.setMinimumWidth(220)
        self.setMaximumWidth(220)

        # Set default active button
        self.set_active_button("dashboard")

    def create_sidebar_button(self, text, icon_path, signal, logout=False):
        """Helper function to create and add a sidebar button."""
        button = SidebarButton(text, icon_path)
        button.clicked.connect(lambda: self.on_button_clicked(text, signal))
        self.layout.addWidget(button)

        if not logout:
            self.buttons[text.lower()] = button  # Store reference to manage active state

        return button

    def on_button_clicked(self, button_name, signal):
        """Handle sidebar button click and set it as active."""
        print(f"{button_name} button clicked")  # Log to console
        self.set_active_button(button_name.lower())  # Update active button
        signal.emit()  # Emit the appropriate signal

    def set_active_button(self, button_name):
        """Set the active button in the sidebar."""
        for name, button in self.buttons.items():
            button.set_active(name == button_name)


class Main_view(QMainWindow):
    logout_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading App")

        # User ID (Not set initially)
        self.user_id = None

        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create sidebar
        self.sidebar = Sidebar()
        self.sidebar.dashboard_clicked.connect(self.show_dashboard)
        self.sidebar.stock_clicked.connect(self.show_stocks)
        self.sidebar.history_clicked.connect(self.show_history)
        self.sidebar.chatbot_clicked.connect(self.show_chatbot)
        self.sidebar.settings_clicked.connect(self.show_settings)
        self.sidebar.logout_clicked.connect(lambda : self.logout_requested.emit())

        # Create content stack
        self.content_stack = QStackedWidget()

        # Create placeholders (Dashboard not yet initialized)
        self.dashboard_widget = DashboardView()
        self.stock_widget = StockView()
        self.history_widget = QWidget()
        self.chatbot_widget = QWidget()
        self.settings_widget = QWidget()

        # Add widgets to stack
        self.content_stack.addWidget(self.dashboard_widget)
        self.content_stack.addWidget(self.stock_widget)
        self.content_stack.addWidget(self.history_widget)
        self.content_stack.addWidget(self.chatbot_widget)
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

        self.main_stack = QStackedWidget()
        self.main_stack.addWidget(self.app_widget)

        # Add main stack to main layout
        self.main_layout.addWidget(self.main_stack)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F8F9FA;
            }
        """)

    def set_user(self, user_id):
        """Initialize the dashboard only when user_id is available"""
        self.user_id = user_id
        self.dashboard_presenter = DashboardPresenter(DashboardModel(), self.dashboard_widget, self.user_id)
        self.show_dashboard()  # Now that the user is set, show dashboard

    def show_dashboard(self):
        """Show the dashboard screen"""
        if self.user_id is None:
            print("User ID not set yet!")  # Debug message
            return

        self.content_stack.setCurrentWidget(self.dashboard_widget)
        self.sidebar.set_active_button("dashboard")

    def show_stocks(self):
        """Show the stocks screen"""
        self.stock_presenter = StockPresenter(StockModel(), self.stock_widget, self.user_id)
        self.content_stack.setCurrentWidget(self.stock_widget)
        self.sidebar.set_active_button("stocks")

    def show_history(self):
        """Show the history screen"""
        # self.history_presenter = HistoryPresenter(HistoryModel(), self.history_widget, self.user_id)
        self.content_stack.setCurrentWidget(self.history_widget)
        self.sidebar.set_active_button("history")

    def show_chatbot(self):
        """Show the chatbot screen"""
        self.content_stack.setCurrentWidget(self.chatbot_widget)
        self.sidebar.set_active_button("chatbot")

    def show_settings(self):
        """Show the settings screen"""
        self.content_stack.setCurrentWidget(self.settings_widget)
        self.sidebar.set_active_button("settings")