from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                              QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Slot, Qt

from Interfaces.ILogin import *

class CombinedMeta(type(QMainWindow), type(ILogin)):
    pass

class LoginWindow(QMainWindow, ILogin, metaclass=CombinedMeta):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Login")
        self.setFixedSize(500, 600)  # Increased window size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QWidget#container {
                background-color: white;
                border-radius: 8px;
            }
            QLabel#title {
                color: #1a73e8;
                font-size: 28px;  /* Increased font size */
                font-weight: bold;
            }
            QLabel {
                color: #333333;
                font-size: 16px;  /* Increased font size */
                margin-bottom: 8px;
            }
            QLineEdit {
                padding: 15px;  /* Increased padding */
                border: 2px solid #dddddd;  /* Thicker border */
                border-radius: 6px;  /* Slightly larger border radius */
                font-size: 16px;  /* Increased font size */
                margin-bottom: 25px;  /* Increased margin */
                min-height: 25px;  /* Ensure minimum height */
                background-color: #f8f9fa;  /* Light background for better visibility */
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
                background-color: white;
                outline: none;
            }
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 6px;  /* Increased border radius */
                padding: 15px;  /* Increased padding */
                font-size: 18px;  /* Increased font size */
                margin-top: 15px;
                min-height: 50px;  /* Ensure minimum height */
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton#forgot_password {
                background-color: transparent;
                color: #1a73e8;
                font-size: 16px;
                min-height: 30px;
            }
            QPushButton#forgot_password:hover {
                text-decoration: underline;
            }
        """)

        # Create main container widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("container")
        self.setCentralWidget(self.central_widget)

        # Create layout with larger margins
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)  # Increased margins
        layout.setSpacing(0)
        self.central_widget.setLayout(layout)

        # Title
        self.label_title = QLabel("Login")
        self.label_title.setObjectName("title")
        self.label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_title)
        layout.addSpacing(40)  # Increased spacing

        # Username field
        self.label_username = QLabel("Email")
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Enter your email")
        self.input_username
        self.input_username.setMinimumWidth(300)  # Ensure minimum width
        layout.addWidget(self.input_username)

        # Password field
        self.label_password = QLabel("Password")
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter your password")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setMinimumWidth(300)  # Ensure minimum width
        layout.addWidget(self.input_password)

        # Add more spacing before button
        layout.addSpacing(10)

        # Login button
        self.btn_login = QPushButton("Log In")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

        # Forgot password button
        self.btn_forgot = QPushButton("Forgot Password?")
        self.btn_forgot.setObjectName("forgot_password")
        self.btn_forgot.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_forgot)
        layout.addSpacing(20)

        # Message label
        self.label_message = QLabel()
        self.label_message.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_message)

        # Center the window
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

    @Slot()
    def login(self):
        self.presenter.login()

    def get_username(self):
        return self.input_username.text()

    def get_password(self):
        return self.input_password.text()

    def show_message(self, message):
        self.label_message.setText(message)