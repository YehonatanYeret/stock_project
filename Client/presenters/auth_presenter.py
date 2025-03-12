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
        # Validate inputs
        if not email or not username or not password:
            self.view.show_error("All fields are required")
            return False
        
        if password != confirm_password:
            self.view.show_error("Passwords do not match")
            return False
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            self.view.show_error("Please enter a valid email address")
            return False
        
        # Prepare registration data
        register_data = {
            "email": email,
            "username": username,
            "password": password
        }
        
        try:
            # Make API call to register endpoint
            response = self.api_service.post("/auth/register", data=register_data)
            
            if response.status_code == 201:  # Assuming 201 for successful creation
                # Extract token and user data
                response_data = response.json()
                token = response_data.get("token")
                user_data = response_data.get("user")
                
                # Update user model with new data
                self.user_model.set_token(token)
                self.user_model.set_user_data(user_data)
                
                # Reset the view
                self.view.clear_error()
                self.view.clear_fields()
                
                return True
            else:
                # Handle failed registration
                error_message = response.json().get("message", "Registration failed. Please try again.")
                self.view.show_error(error_message)
                return False
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
            return False
    
    def logout(self):
        """Log out the current user by clearing user data"""
        self.user_model.clear_user_data()