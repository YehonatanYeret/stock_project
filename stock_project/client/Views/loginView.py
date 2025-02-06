import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QStackedWidget
)
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QParallelAnimationGroup, Slot

# Interface for Login and Signup functionality
class ILogin:
    """ 
    Interface defining the structure for authentication methods.
    This should be implemented by any class handling user login/signup.
    """
    def get_username(self): pass
    def get_password(self): pass
    def show_signin_message(self, message): pass
    def get_signup_username(self): pass
    def get_signup_password(self): pass
    def show_signup_message(self, message): pass

# CombinedMeta ensures proper multiple inheritance handling
class CombinedMeta(type(QMainWindow), type(ILogin)):
    """ 
    Metaclass to handle multiple inheritance of QMainWindow and ILogin.
    Resolves potential conflicts between QObject-based and non-QObject-based classes.
    """
    pass

class LoginWindow(QMainWindow, ILogin, metaclass=CombinedMeta):
    """
    LoginWindow provides an interactive UI for user authentication.
    
    Features:
    - Two forms: Login & Signup, managed via QStackedWidget.
    - Animated transitions for smooth user experience.
    - Modern UI styling using QSS (Qt Style Sheets).
    - Handles user input and displays messages.
    """
    def __init__(self):
        """
        Initialize the LoginWindow, set up UI elements and animations.
        """
        super().__init__()
        self.setWindowTitle("Login/Signup")
        self.setFixedSize(800, 600)  # Fixed window size for better layout management
        self.setup_ui()
        self.apply_styles()  # Apply QSS styling
        self.center_window()  # Center window on screen
        self.is_login = True  # Track if current form is login (True) or signup (False)
        self.animation_group = None  # Store animation instance for smooth transitions

    def apply_styles(self):
        """
        Apply modern styling using QSS.
        This improves visual appeal with consistent colors, borders, and animations.
        """
        style = """
            QMainWindow {
                background-color: #f8fafc;
            }
            QWidget#container {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
            QLabel#title {
                color: #1e293b;
                font-size: 28px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 12px 16px;
                border: 1.5px solid #e2e8f0;
                border-radius: 6px;
                font-size: 15px;
                margin: 6px 0;
                background-color: white;
                color: #1e293b;
                min-height: 45px;
            }
            QPushButton#form_button {
                background-color: #3b82f6;
                color: white;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                min-height: 48px;
                border: none;
            }
        """
        self.setStyleSheet(style)
        self.setLayoutDirection(Qt.RightToLeft)  # Support for right-to-left languages

    def setup_ui(self):
        """
        Set up the main UI components, including forms and layout structure.
        """
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.container = QWidget(self.central_widget)
        self.container.setObjectName("container")
        self.container.setGeometry(0, 0, 800, 600)

        # QStackedWidget manages login and signup forms dynamically
        self.form_stack = QStackedWidget(self.container)
        self.form_stack.setGeometry(0, 0, 500, 600)

        # Setup individual forms
        self.login_widget = QWidget()
        self.setup_login_form()
        self.form_stack.addWidget(self.login_widget)

        self.signup_widget = QWidget()
        self.setup_signup_form()
        self.form_stack.addWidget(self.signup_widget)

    def setup_login_form(self):
        """
        Create the login form with email, password fields, and a sign-in button.
        """
        layout = QVBoxLayout(self.login_widget)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Sign In")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addSpacing(20)

        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Email")
        layout.addWidget(self.login_email)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password)

        login_button = QPushButton("Sign In")
        login_button.setObjectName("form_button")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

    def setup_signup_form(self):
        """
        Create the signup form with email, password fields, and a sign-up button.
        """
        layout = QVBoxLayout(self.signup_widget)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Create Account")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addSpacing(20)

        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Email")
        layout.addWidget(self.signup_email)

        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.signup_password)

        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("form_button")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

    def center_window(self):
        """
        Center the window on the user's screen.
        """
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2,
                  (screen.height() - self.height()) // 2)

    @Slot()
    def login(self):
        """
        Handle the Sign In button click event.
        Delegates login logic to the presenter.
        """
        self.presenter.login()

    @Slot()
    def signup(self):
        """
        Handle the Sign Up button click event.
        Delegates signup logic to the presenter.
        """
        self.presenter.signup()
