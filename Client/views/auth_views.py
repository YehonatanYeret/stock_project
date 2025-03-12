from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from views.components.styled_widgets import (
    PrimaryButton, SecondaryButton, StyledLineEdit, StyledLabel, Card
)

class AuthWidget(QWidget):
    """Base authentication widget with common UI elements"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        
        # Center content in a card
        self.card = Card()
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)
        
        # Logo at the top
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        # In a real app, you would have a logo image
        # self.logo_label.setPixmap(QPixmap("path/to/logo.png"))
        self.logo_label.setText("📈 STOCK PORTFOLIO")
        self.logo_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #4C6FFF;
            }
        """)
        self.card_layout.addWidget(self.logo_label)
        
        # Add some spacing
        self.card_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Error message label (hidden by default)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("""
            QLabel {
                color: #FF5252;
                font-size: 14px;
                background-color: #FFEBEE;
                border-radius: 4px;
                padding: 10px;
                border: 1px solid #FFCDD2;
            }
        """)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False)
        self.card_layout.addWidget(self.error_label)
        
        # Form container - will be filled by subclasses
        self.form_container = QWidget()
        self.form_layout = QVBoxLayout(self.form_container)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)
        self.card_layout.addWidget(self.form_container)
        
        # Add some spacing
        self.card_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Center the card in the main layout with spacers
        h_layout = QHBoxLayout()
        h_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        h_layout.addWidget(self.card)
        h_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        v_layout = QVBoxLayout()
        v_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        v_layout.addLayout(h_layout)
        v_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.layout.addLayout(v_layout)
    
    def show_error(self, message):
        """Show an error message"""
        self.error_label.setText(message)
        self.error_label.setVisible(True)
    
    def clear_error(self):
        """Clear the error message"""
        self.error_label.setVisible(False)

class LoginWidget(AuthWidget):
    """Login widget for user authentication"""
    login_requested = Signal(str, str)
    register_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set title
        self.title_label = StyledLabel("Log in to your account", is_title=True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.form_layout.addWidget(self.title_label)
        
        # Email field
        self.email_label = StyledLabel("Email")
        self.form_layout.addWidget(self.email_label)
        
        self.email_input = StyledLineEdit(placeholder="Enter your email")
        self.form_layout.addWidget(self.email_input)
        
        # Password field
        self.password_label = StyledLabel("Password")
        self.form_layout.addWidget(self.password_label)
        
        self.password_input = StyledLineEdit(placeholder="Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.password_input)
        
        # Login button
        self.login_button = PrimaryButton("Log In")
        self.login_button.clicked.connect(self.on_login_clicked)
        self.form_layout.addWidget(self.login_button)
        
        # Register link
        register_layout = QHBoxLayout()
        register_layout.addStretch()
        register_label = StyledLabel("Don't have an account?")
        register_layout.addWidget(register_label)
        
        self.register_button = QPushButton("Register")
        self.register_button.setFlat(True)
        self.register_button.setStyleSheet("""
            QPushButton {
                color: #4C6FFF;
                font-size: 14px;
                font-weight: bold;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.register_button.clicked.connect(self.on_register_clicked)
        register_layout.addWidget(self.register_button)
        register_layout.addStretch()
        
        self.form_layout.addLayout(register_layout)
        
        # Set fixed card size
        self.card.setMinimumWidth(400)
        self.card.setMaximumWidth(400)
    
    def on_login_clicked(self):
        """Handle login button click"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        # Basic validation
        if not email:
            self.show_error("Please enter your email")
            return
        
        if not password:
            self.show_error("Please enter your password")
            return
        
        self.clear_error()
        self.login_requested.emit(email, password)
    
    def on_register_clicked(self):
        """Handle register button click"""
        self.register_requested.emit()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.email_input.clear()
        self.password_input.clear()
        self.clear_error()

class RegisterWidget(AuthWidget):
    """Registration widget for new users"""
    register_requested = Signal(str, str, str)
    login_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set title
        self.title_label = StyledLabel("Create a new account", is_title=True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.form_layout.addWidget(self.title_label)
        
        # Email field
        self.email_label = StyledLabel("Email")
        self.form_layout.addWidget(self.email_label)
        
        self.email_input = StyledLineEdit(placeholder="Enter your email")
        self.form_layout.addWidget(self.email_input)
        
        # Username field
        self.username_label = StyledLabel("Username")
        self.form_layout.addWidget(self.username_label)
        
        self.username_input = StyledLineEdit(placeholder="Choose a username")
        self.form_layout.addWidget(self.username_input)
        
        # Password field
        self.password_label = StyledLabel("Password")
        self.form_layout.addWidget(self.password_label)
        
        self.password_input = StyledLineEdit(placeholder="Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.password_input)
        
        # Confirm password field
        self.confirm_password_label = StyledLabel("Confirm Password")
        self.form_layout.addWidget(self.confirm_password_label)
        
        self.confirm_password_input = StyledLineEdit(placeholder="Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.confirm_password_input)
        
        # Register button
        self.register_button = PrimaryButton("Register")
        self.register_button.clicked.connect(self.on_register_clicked)
        self.form_layout.addWidget(self.register_button)
        
        # Login link
        login_layout = QHBoxLayout()
        login_layout.addStretch()
        login_label = StyledLabel("Already have an account?")
        login_layout.addWidget(login_label)
        
        self.login_button = QPushButton("Log In")
        self.login_button.setFlat(True)
        self.login_button.setStyleSheet("""
            QPushButton {
                color: #4C6FFF;
                font-size: 14px;
                font-weight: bold;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.login_button.clicked.connect(self.on_login_clicked)
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()
        
        self.form_layout.addLayout(login_layout)
        
        # Set fixed card size
        self.card.setMinimumWidth(400)
        self.card.setMaximumWidth(400)
    
    def on_register_clicked(self):
        """Handle register button click"""
        email = self.email_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Basic validation
        if not email:
            self.show_error("Please enter your email")
            return
        
        if not username:
            self.show_error("Please enter a username")
            return
        
        if not password:
            self.show_error("Please enter a password")
            return
        
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
        
        self.clear_error()
        self.register_requested.emit(email, username, password)
    
    def on_login_clicked(self):
        """Handle login button click"""
        self.login_requested.emit()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.email_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.clear_error()

class AuthStackedWidget(QStackedWidget):
    """Stacked widget for switching between login and registration"""
    login_requested = Signal(str, str)
    register_requested = Signal(str, str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create login and register widgets
        self.login_widget = LoginWidget()
        self.register_widget = RegisterWidget()
        
        # Add widgets to the stack
        self.addWidget(self.login_widget)
        self.addWidget(self.register_widget)
        
        # Connect signals
        self.login_widget.login_requested.connect(self.login_requested)
        self.login_widget.register_requested.connect(self.show_register)
        
        self.register_widget.register_requested.connect(self.register_requested)
        self.register_widget.login_requested.connect(self.show_login)
        
        # Set login as the default view
        self.setCurrentWidget(self.login_widget)
    
    def show_login(self):
        """Show the login widget"""
        self.login_widget.clear_fields()
        self.setCurrentWidget(self.login_widget)
    
    def show_register(self):
        """Show the register widget"""
        self.register_widget.clear_fields()
        self.setCurrentWidget(self.register_widget)
    
    def show_error(self, message):
        """Show an error message on the current widget"""
        current_widget = self.currentWidget()
        if hasattr(current_widget, 'show_error'):
            current_widget.show_error(message)