from services.api_service import ApiService
from PySide6.QtCore import Signal


class AuthPresenter:
    """
    Presenter for handling authentication logic
    """
    def __init__(self, auth_view, auth_model, api_service=None):
        """
        Initialize the auth presenter
        
        Args:
            auth_view: The authentication view (must have show_error, clear_error methods)
            user_model: The user model to update after authentication
            api_service: Optional ApiService instance (will create one if not provided)
        """
        self.view = auth_view
        self.model = auth_model
        self.api_service = api_service if api_service else ApiService()
        self.view.login_attempted.connect(self.login)
        self.view.register_attempted.connect(self.register)
        self.model.completed.connect(self.view.completed)

    def login(self, email, password):
        """
        Handle login process
        
        Args:
            email: User's email
            password: User's password
        """
        message = self.model.authenticate(email, password)
        self.view.show_error(message)  # Display error from server

    def register(self, email, username, password, confirm_password):
        """
        Handle registration process
        
        Args:
            email: User's email
            username: User's username
            password: User's password
            confirm_password: Password confirmation
        """
        message = self.model.signup(email, username, password, confirm_password)
        self.view.show_error(message)

    def logout(self):
        """Log out the current user by clearing user data"""
        self.user_model.clear_user_data()