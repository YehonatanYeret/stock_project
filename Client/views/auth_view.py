from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QStackedWidget, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal

from views.components.styled_widgets import (
    PrimaryButton, StyledLineEdit, StyledLabel, Card
)

class AuthWidget(QWidget):
    """Base authentication widget with common UI elements."""
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        
        # Card container
        self.card = Card()
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)
        
        # Logo
        self.logo_label = self.create_logo()
        self.card_layout.addWidget(self.logo_label)
        
        # Spacer
        self.card_layout.addItem(self.create_spacer())
        
        # Error label (hidden by default)
        self.error_label = self.create_error_label()
        self.card_layout.addWidget(self.error_label)
        
        # Title label
        self.title_label = StyledLabel(title, is_title=True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(self.title_label)
        
        # Form container (to be populated by subclasses)
        self.form_container = QWidget()
        self.form_layout = QVBoxLayout(self.form_container)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)
        self.card_layout.addWidget(self.form_container)
        
        # Spacer
        self.card_layout.addItem(self.create_spacer())
        
        # Center the card in the main layout
        self.layout.addLayout(self.center_card(self.card))
    
    def create_logo(self):
        """Return a QLabel for the app logo."""
        label = QLabel("📈 STOCK PORTFOLIO")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4C6FFF;")
        return label
    
    def create_error_label(self):
        """Return an error message QLabel (initially hidden)."""
        label = QLabel()
        label.setStyleSheet("""
            QLabel {
                color: #FF5252;
                font-size: 14px;
                background-color: #FFEBEE;
                border-radius: 4px;
                padding: 10px;
                border: 1px solid #FFCDD2;
            }
        """)
        label.setAlignment(Qt.AlignCenter)
        label.setVisible(False)
        return label
    
    def create_spacer(self):
        """Return a vertical spacer item."""
        return QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    
    def center_card(self, widget):
        """Return a layout that centers the given widget."""
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(widget)
        h_layout.addStretch()
        
        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addLayout(h_layout)
        v_layout.addStretch()
        return v_layout
    
    def add_form_field(self, label_text, placeholder, echo_mode=None):
        """Helper: Add a labeled input field to the form layout."""
        label = StyledLabel(label_text)
        self.form_layout.addWidget(label)
        
        input_field = StyledLineEdit(placeholder=placeholder)
        if echo_mode:
            input_field.setEchoMode(echo_mode)
        self.form_layout.addWidget(input_field)
        return input_field
    
    def create_auth_link(self, label_text, button_text, callback):
        """Helper: Create a horizontal layout for auth links."""
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(StyledLabel(label_text))
        
        button = QPushButton(button_text)
        button.setFlat(True)
        button.setStyleSheet("""
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
        button.clicked.connect(callback)
        layout.addWidget(button)
        layout.addStretch()
        return layout
    
    def show_error(self, message):
        """Display an error message."""
        print(message)
        self.error_label.setText(message)
        self.error_label.setVisible(True)
    
    def clear_error(self):
        """Hide the error message."""
        self.error_label.setVisible(False)


class LoginWidget(AuthWidget):
    """Login widget for user authentication."""
    # Signal emitted when a valid login attempt occurs
    login_attempt = Signal(str, str)
    # Signal emitted to switch to the registration view
    switch_to_register = Signal()

    def __init__(self, parent=None):
        super().__init__("Log in to your account", parent)
        
        # Email input field
        self.email_input = self.add_form_field("Email", "Enter your email")
        # Password input field
        self.password_input = self.add_form_field("Password", "Enter your password", QLineEdit.Password)
        
        # Login button
        self.login_button = PrimaryButton("Log In")
        self.login_button.clicked.connect(self.on_login_clicked)
        self.form_layout.addWidget(self.login_button)
        
        # Link to switch to the registration view
        self.form_layout.addLayout(self.create_auth_link("Don't have an account?", "Register", self.on_switch_to_register))
        
        # Fixed card width for consistency
        self.card.setFixedWidth(400)
    
    def validate_inputs(self):
        """Check that email and password are provided."""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        if not email:
            self.show_error("Please enter your email")
            return False
        if not password:
            self.show_error("Please enter your password")
            return False
        self.clear_error()
        return True
    
    def on_login_clicked(self):
        """Handle login button click after validating inputs."""
        if self.validate_inputs():
            email = self.email_input.text().strip()
            password = self.password_input.text()
            # (Optional) Insert additional authentication logic here.
            self.login_attempt.emit(email, password)
    
    def on_switch_to_register(self):
        """Signal a view change to the registration screen."""
        self.switch_to_register.emit()


class RegisterWidget(AuthWidget):
    """Registration widget for new users."""
    # Signal emitted when a valid registration attempt occurs
    register_attempt = Signal(str, str, str, str)
    # Signal emitted to switch back to the login view
    switch_to_login = Signal()

    def __init__(self, parent=None):
        super().__init__("Create a new account", parent)
        
        # Email input field
        self.email_input = self.add_form_field("Email", "Enter your email")
        # Username input field
        self.username_input = self.add_form_field("Username", "Choose a username")
        # Password input field
        self.password_input = self.add_form_field("Password", "Create a password", QLineEdit.Password)
        # Confirm password input field
        self.confirm_password_input = self.add_form_field("Confirm Password", "Confirm your password", QLineEdit.Password)
        
        # Register button
        self.register_button = PrimaryButton("Register")
        self.register_button.clicked.connect(self.on_register_clicked)
        self.form_layout.addWidget(self.register_button)
        
        # Link to switch to the login view
        self.form_layout.addLayout(self.create_auth_link("Already have an account?", "Log In", self.on_switch_to_login))
        
        # Fixed card width for consistency
        self.card.setFixedWidth(400)
    
    def validate_inputs(self):
        """Check that all registration fields are correctly filled."""
        email = self.email_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not email:
            self.show_error("Please enter your email")
            return False
        if not username:
            self.show_error("Please enter a username")
            return False
        if not password:
            self.show_error("Please enter your password")
            return False
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return False
        
        self.clear_error()
        return True
    
    def on_register_clicked(self):
        """Handle registration button click after validating inputs."""
        if self.validate_inputs():
            email = self.email_input.text().strip()
            username = self.username_input.text().strip()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()
            self.register_attempt.emit(email, username, password, confirm_password)
    
    def on_switch_to_login(self):
        """Signal a view change to the login screen."""
        self.switch_to_login.emit()


class Auth_view(QStackedWidget):
    """Encapsulation widget for login and registration views.
    Emits a `completed` signal when authentication (login or registration)
    is successfully validated.
    """
    completed = Signal(int)
    login_attempted = Signal(str, str)
    register_attempted = Signal(str, str, str, str)
    

    def __init__(self, parent=None):
        super().__init__(parent)
        self.login_widget = LoginWidget()
        self.register_widget = RegisterWidget()
        
        self.addWidget(self.login_widget)
        self.addWidget(self.register_widget)
        
        # Start with the login view 
        self.setCurrentWidget(self.login_widget)
        
        # Connect view-switch 
        self.login_widget.login_attempt.connect(self.login_attempted)
        self.register_widget.register_attempt.connect(self.register_attempted)

        self.login_widget.switch_to_register.connect(self.show_register)
        self.register_widget.switch_to_login.connect(self.show_login)

    def show_error(self, message):
        """Display an error message."""
        self.currentWidget().show_error(message)

    def show_register(self):
        """Switch to the registration view."""
        self.login_widget.clear_error()
        self.setCurrentWidget(self.register_widget)
    
    def show_login(self):
        """Switch to the login view."""
        self.register_widget.clear_error()
        self.setCurrentWidget(self.login_widget)

    def clear_error(self):
        """Hide the error message."""
        self.currentWidget().clear_error()