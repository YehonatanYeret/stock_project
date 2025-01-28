from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                              QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget)
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, Property, QEasingCurve, QParallelAnimationGroup, Slot
from PySide6.QtGui import QColor, QPalette
from Interfaces.ILogin import *

class CombinedMeta(type(QMainWindow), type(ILogin)):
    pass

class AnimatedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._pos = QPoint()

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos
        self.move(pos)

    pos_prop = Property(QPoint, get_pos, set_pos)

class LoginWindow(QMainWindow, ILogin, metaclass=CombinedMeta):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Signup")
        self.setFixedSize(800, 500)

        # Set solid background for main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a73e8;
            }
            QWidget#container {
                background-color: white;
                border-radius: 10px;
            }
            QLabel#title {
                color: #1a73e8;
                font-size: 24px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #dddddd;
                border-radius: 4px;
                font-size: 14px;
                margin: 5px 0;
                background-color: white;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
                background-color: white;
            }
            QPushButton#form_button {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px;
                font-size: 16px;
                margin: 10px 0;
                min-height: 45px;
            }
            QPushButton#form_button:hover {
                background-color: #1557b0;
            }
            QWidget#side_panel {
                background-color: #1557b0;
                border-radius: 10px;
            }
            QLabel#side_title {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            QLabel#side_text {
                color: white;
                font-size: 14px;
            }
            QPushButton#side_button {
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 4px;
                padding: 12px 30px;
                font-size: 16px;
                min-height: 45px;
            }
            QPushButton#side_button:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout()
        self.central_widget.setLayout(layout)
        
        # Container
        self.container = QWidget()
        self.container.setObjectName("container")
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Forms stack
        self.form_stack = QStackedWidget()
        
        # Login form
        login_widget = AnimatedWidget()
        login_layout = QVBoxLayout(login_widget)
        login_layout.setContentsMargins(40, 40, 40, 40)
        
        login_title = QLabel("Sign In")
        login_title.setObjectName("title")
        login_layout.addWidget(login_title)
        login_layout.addSpacing(20)
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Email")
        self.login_email.setMinimumHeight(45)
        login_layout.addWidget(self.login_email)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(45)
        login_layout.addWidget(self.login_password)
        
        login_button = QPushButton("Sign In")
        login_button.clicked.connect(self.login)
        login_button.setObjectName("form_button")
        login_layout.addWidget(login_button)

        self.sign_in_massage = QLabel()
        self.sign_in_massage.setAlignment(Qt.AlignCenter)
        self.sign_in_massage.setStyleSheet("color: red; font-size: 14px;")  # Optional styling
        login_layout.addWidget(self.sign_in_massage)
        
        login_layout.addStretch()
        self.form_stack.addWidget(login_widget)
        
        # Signup form
        signup_widget = AnimatedWidget()
        signup_layout = QVBoxLayout(signup_widget)
        signup_layout.setContentsMargins(40, 40, 40, 40)
        
        signup_title = QLabel("Create Account")
        signup_title.setObjectName("title")
        signup_layout.addWidget(signup_title)
        signup_layout.addSpacing(20)
        
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Email")
        self.signup_email.setMinimumHeight(45)
        signup_layout.addWidget(self.signup_email)
        
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setMinimumHeight(45)
        signup_layout.addWidget(self.signup_password)
        
        signup_button = QPushButton("Sign Up")
        signup_button.setObjectName("form_button")
        signup_button.clicked.connect(self.signup)
        signup_layout.addWidget(signup_button)

        self.sign_up_massage = QLabel()
        self.sign_up_massage.setAlignment(Qt.AlignCenter)
        self.sign_up_massage.setStyleSheet("color: red; font-size: 14px;")  # Optional styling
        signup_layout.addWidget(self.sign_up_massage)
        
        signup_layout.addStretch()
        self.form_stack.addWidget(signup_widget)
        
        container_layout.addWidget(self.form_stack)
        
        # Side panel
        self.side_panel = QWidget()
        self.side_panel.setObjectName("side_panel")
        self.side_panel.setFixedWidth(300)
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setContentsMargins(40, 40, 40, 40)
        side_layout.setAlignment(Qt.AlignCenter)
        
        side_title = QLabel("New Here?")
        side_title.setObjectName("side_title")
        side_layout.addWidget(side_title, alignment=Qt.AlignCenter)
        
        side_text = QLabel("Sign up and discover great opportunities!")
        side_text.setObjectName("side_text")
        side_text.setWordWrap(True)
        side_layout.addWidget(side_text, alignment=Qt.AlignCenter)
        
        toggle_button = QPushButton("Sign Up")
        toggle_button.setObjectName("side_button")
        toggle_button.clicked.connect(self.toggle_form)
        side_layout.addWidget(toggle_button, alignment=Qt.AlignCenter)
        
        container_layout.addWidget(self.side_panel)
        
        # Add container to main layout
        layout.addWidget(self.container)

        # Center window
        self.center_window()
        
        # Initialize states
        self.is_login = True
        self.animation_group = None
        self.side_panel.move(500, 0)  # Initial position

    @Slot()
    def login(self):
        self.presenter.login()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

    def toggle_form(self):
        if self.animation_group and self.animation_group.state() == QParallelAnimationGroup.Running:
            return
            
        self.animation_group = QParallelAnimationGroup()
        
        # Side panel animation
        side_anim = QPropertyAnimation(self.side_panel, b"pos")
        side_anim.setDuration(500)
        side_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Form animation
        form_anim = QPropertyAnimation(self.form_stack, b"pos")
        form_anim.setDuration(500)
        form_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        if self.is_login:
            side_anim.setStartValue(QPoint(500, 0))
            side_anim.setEndValue(QPoint(0, 0))
            form_anim.setStartValue(QPoint(0, 0))
            form_anim.setEndValue(QPoint(300, 0))
            
            self.side_panel.findChild(QLabel, "side_title").setText("One of Us?")
            self.side_panel.findChild(QLabel, "side_text").setText("If you already have an account, just sign in!")
            self.side_panel.findChild(QPushButton, "side_button").setText("Sign In")
            self.form_stack.setCurrentIndex(1)
        else:
            side_anim.setStartValue(QPoint(0, 0))
            side_anim.setEndValue(QPoint(500, 0))
            form_anim.setStartValue(QPoint(300, 0))
            form_anim.setEndValue(QPoint(0, 0))
            
            self.side_panel.findChild(QLabel, "side_title").setText("New Here?")
            self.side_panel.findChild(QLabel, "side_text").setText("Sign up and discover great opportunities!")
            self.side_panel.findChild(QPushButton, "side_button").setText("Sign Up")
            self.form_stack.setCurrentIndex(0)
        
        self.animation_group.addAnimation(side_anim)
        self.animation_group.addAnimation(form_anim)
        self.animation_group.start()
        
        self.is_login = not self.is_login

    def get_username(self):
        return self.login_email.text()

    def get_password(self):
        return self.login_password.text()

    def show_signin_message(self, message):
        self.sign_in_massage.setText(message)

    @Slot()
    def signup(self):
        self.presenter.signup()

    def get_signup_username(self):
        return self.signup_email.text()

    def get_signup_password(self):
        return self.signup_password.text()

    def show_signup_message(self, message):
        self.sign_up_massage.setText(message)