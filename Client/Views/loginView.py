import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QStackedWidget
)
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QParallelAnimationGroup, Slot
from Interfaces.ILogin import ILogin

# CombinedMeta for multiple inheritance.
class CombinedMeta(type(QMainWindow), type(ILogin)):
    pass

class LoginWindow(QMainWindow, ILogin, metaclass=CombinedMeta):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Signup")
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.apply_styles()   # Apply QSS styles
        self.center_window()
        self.is_login = True  # Flag to determine if we are in login mode
        self.animation_group = None  # Holds animations for the transition

    def apply_styles(self):
        """
        Applies styles (QSS) to the main window and its widgets.
        This includes colors, borders, and other visual aspects.
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
                letter-spacing: -0.3px;
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
            
            QLineEdit:focus {
                border: 1.5px solid #60a5fa;
                background-color: white;
            }
            
            QLineEdit[error="true"] {
                border: 1.5px solid #ef4444;
                background-color: #fef2f2;
            }
            
            QLineEdit[error="true"]:focus {
                border: 1.5px solid #ef4444;
                background-color: white;
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
            
            QPushButton#form_button:hover {
                background-color: #2563eb;
            }
            
            QPushButton#form_button:pressed {
                background-color: #1d4ed8;
            }
            
            QWidget#side_panel {
                background-color: #3b82f6;
                border-radius: 12px;
            }
            
            QLabel#side_title {
                color: white;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: -0.3px;
            }
            
            QLabel#side_text {
                color: rgba(255, 255, 255, 0.95);
                font-size: 15px;
                padding: 12px;
                line-height: 1.4;
            }
            
            QPushButton#side_button {
                background-color: transparent;
                color: white;
                border: 1.5px solid white;
                border-radius: 6px;
                padding: 12px 32px;
                font-size: 16px;
                min-height: 48px;
                font-weight: bold;
                margin: 12px 0;
            }
            
            QPushButton#side_button:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            QPushButton#side_button:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
            
            QLabel {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }

            QLabel#error_message,
            QLabel#sign_in_message, 
            QLabel#sign_up_message {
                background-color: #fef2f2;
                color: #dc2626;
                border: 1px solid #fecaca;
                border-radius: 6px;
                padding: 12px 16px;
                font-size: 15px;
                font-weight: 500;
                margin: 12px 0;
                qproperty-alignment: AlignCenter;
                min-height: 24px;
                letter-spacing: 0.2px;
            }

            QLabel#error_message:empty,
            QLabel#sign_in_message:empty, 
            QLabel#sign_up_message:empty {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
        """
        self.setStyleSheet(style)

        # Set layout direction for RTL support
        self.setLayoutDirection(Qt.RightToLeft)

    def setup_ui(self):
        """
        Set up the UI with absolute positioning for animated widgets.
        The UI includes a container, a form stack for login and signup forms,
        and a side panel for toggling between the two forms.
        """
        # Main central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
       
        self.container = QWidget(self.central_widget)
        self.container.setObjectName("container")
        self.container.setGeometry(0, 0, 800, 600)
       
        self.form_stack = QStackedWidget(self.container)
        self.form_stack.setGeometry(0, 0, 500, 600)
       
        self.login_widget = QWidget()
        self.setup_login_form()
        self.form_stack.addWidget(self.login_widget)
       
        self.signup_widget = QWidget()
        self.setup_signup_form()
        self.form_stack.addWidget(self.signup_widget)
       
        self.side_panel = QWidget(self.container)
        self.side_panel.setObjectName("side_panel")
        self.side_panel.setGeometry(500, 0, 300, 600)
        self.setup_side_panel()

    def setup_login_form(self):
        """
        Build the login form with email and password inputs and a sign in button.
        """
        layout = QVBoxLayout(self.login_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("Sign In")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addSpacing(20)
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Email")
        self.login_email.setMinimumHeight(45)
        layout.addWidget(self.login_email)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(45)
        layout.addWidget(self.login_password)
        
        login_button = QPushButton("Sign In")
        login_button.setObjectName("form_button")
        login_button.clicked.connect(self.signin)
        layout.addWidget(login_button)
        
        self.sign_in_message = QLabel()
        self.sign_in_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sign_in_message)
        layout.addStretch()

    def setup_signup_form(self):
        """
        Build the signup form with username, email, and password inputs and a sign up button.
        """
        layout = QVBoxLayout(self.signup_widget)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Create Account")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addSpacing(20)

        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText("Username")
        self.signup_username.setMinimumHeight(45)
        layout.addWidget(self.signup_username)

        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Email")
        self.signup_email.setMinimumHeight(45)
        layout.addWidget(self.signup_email)

        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setMinimumHeight(45)
        layout.addWidget(self.signup_password)

        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("form_button")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        self.sign_up_message = QLabel()
        self.sign_up_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sign_up_message)
        layout.addStretch()

    def setup_side_panel(self):
        """
        Build the side panel used to toggle between login and signup forms.
        """
        layout = QVBoxLayout(self.side_panel)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        self.side_title = QLabel("New Here?")
        self.side_title.setObjectName("side_title")
        layout.addWidget(self.side_title, alignment=Qt.AlignCenter)
        
        self.side_text = QLabel("Sign up and discover great opportunities!")
        self.side_text.setObjectName("side_text")
        self.side_text.setWordWrap(True)
        layout.addWidget(self.side_text, alignment=Qt.AlignCenter)
        
        self.side_button = QPushButton("Sign Up")
        self.side_button.setObjectName("side_button")
        self.side_button.clicked.connect(self.toggle_form)
        layout.addWidget(self.side_button, alignment=Qt.AlignCenter)

    def center_window(self):
        """
        Center the window on the primary screen.
        """
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2,
                  (screen.height() - self.height()) // 2)

    @Slot()
    def signin(self):
        """
        Called when the Sign In button is pressed.
        Delegates action to the presenter.
        """
        self.presenter.signin()

    @Slot()
    def signup(self):
        """
        Called when the Sign Up button is pressed.
        Delegates action to the presenter.
        """
        self.presenter.signup()

    def toggle_form(self):
        """
        Toggle between login and signup forms with smooth slide animations.
        The method animates both the form_stack and the side_panel simultaneously.
        """
        if self.animation_group and self.animation_group.state() == QParallelAnimationGroup.Running:
            return

        self.animation_group = QParallelAnimationGroup()

        # Animate the side panel movement
        side_anim = QPropertyAnimation(self.side_panel, b"pos")
        side_anim.setDuration(300)
        side_anim.setEasingCurve(QEasingCurve.InOutQuad)

        # Animate the form stack movement
        form_anim = QPropertyAnimation(self.form_stack, b"pos")
        form_anim.setDuration(300)
        form_anim.setEasingCurve(QEasingCurve.InOutQuad)

        if self.is_login:
            # Transition from login to signup
            side_anim.setEndValue(QPoint(0, 0))
            form_anim.setEndValue(QPoint(300, 0))
            self.side_title.setText("One of Us?")
            self.side_text.setText("If you already have an account, just sign in.\nWe've missed you!")
            self.side_button.setText("Sign In")
            self.form_stack.setCurrentIndex(1)
        else:
            # Transition from signup to login
            side_anim.setEndValue(QPoint(500, 0))
            form_anim.setEndValue(QPoint(0, 0))
            self.side_title.setText("New Here?")
            self.side_text.setText("Sign up and discover great opportunities!")
            self.side_button.setText("Sign Up")
            self.form_stack.setCurrentIndex(0)

        self.animation_group.addAnimation(side_anim)
        self.animation_group.addAnimation(form_anim)
        self.animation_group.start()

        self.is_login = not self.is_login

    # ILogin interface methods
    def get_email(self):
        return self.login_email.text()

    def get_password(self):
        return self.login_password.text()

    def get_signup_email(self):
        return self.signup_email.text()

    def get_signup_password(self):
        return self.signup_password.text()

    def get_signup_username(self):
        return self.signup_username.text()

    def show_signin_message(self, message):
       """
       Enhanced error message display for sign in
       """
       self.sign_in_message.setText(message)
       if message:  # If there's an error message
           self.login_email.setProperty("error", True)
           self.login_password.setProperty("error", True)
       else:
           self.login_email.setProperty("error", False)
           self.login_password.setProperty("error", False)
       
       # Force style refresh
       self.login_email.style().unpolish(self.login_email)
       self.login_email.style().polish(self.login_email)
       self.login_password.style().unpolish(self.login_password)
       self.login_password.style().polish(self.login_password)

    def show_signup_message(self, message):
        """
        Enhanced error message display for sign up
        """
        self.sign_up_message.setText(message)
        if message:  # If there's an error message
            self.signup_email.setProperty("error", True)
            self.signup_username.setProperty("error", True)
            self.signup_password.setProperty("error", True)
        else:
            self.signup_email.setProperty("error", False)
            self.signup_username.setProperty("error", False)
            self.signup_password.setProperty("error", False)
        
        # Force style refresh
        self.signup_email.style().unpolish(self.signup_email)
        self.signup_email.style().polish(self.signup_email)
        self.signup_password.style().unpolish(self.signup_password)
        self.signup_password.style().polish(self.signup_password)
        self.signup_username.style().unpolish(self.signup_username)
        self.signup_username.style().polish(self.signup_username)

