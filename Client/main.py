import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QStackedWidget
)
from PySide6.QtCore import Signal

from views.auth_view import Auth_view
from presenters.auth_presenter import AuthPresenter
from models.auth_model import AuthModel
from views.main_view import Main_view

from services.api_service import ApiService

from presenters.main_presenter import MainPresenter


class MainWindow(QMainWindow):
    """Main application window"""
    # Authentication signals
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
        self.auth_view = Auth_view()
        self.auth_view.presenter = AuthPresenter(self.auth_view, AuthModel(), ApiService())
        self.auth_view.completed.connect(self.show_app)
    
        # Main application widget
        self.app_widget = Main_view()
        self.app_widget.logout_requested.connect(self.show_auth)

        # Main stacked widget to switch between auth and app
        self.main_stack = QStackedWidget()
        self.main_stack.addWidget(self.auth_view)
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
        self.main_stack.setCurrentWidget(self.auth_view)
        self.auth_view.clear_error()

    def show_app(self, user_id):
        """Show the main application screen"""
        print(f"User authenticated: {user_id}")
        self.main_stack.setCurrentWidget(self.app_widget)
        self.app_widget.set_user(user_id)


def main():
    # Create application
    app = QApplication(sys.argv)

    # Create views
    main_window = MainWindow()

    # Show main window in full screen
    main_window.showMaximized()

    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
