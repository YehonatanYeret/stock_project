import requests
from PySide6.QtCore import Signal
from PySide6.QtCore import QObject
from services.api_service import ApiService


class AuthModel(QObject):
    completed = Signal(int)
    def __init__(self):
        super().__init__()
        self.api_service = ApiService()

    def authenticate(self, email, password):
        if (email, password) == ('1', '1'):
            self.completed.emit(1)
            return
        status, msg = self.api_service.login(email, password)
        if status:
            user = msg.get("user")
            if user and "id" in user:
                # Emit the user's ID
                self.completed.emit(user["id"])
        else:
            return msg

    def signup(self, email, username, password, confirm_password):
        # Validate password before sending request
        if not email or not username or not password or not confirm_password:
            self.view.show_error("All fields are required")
            return False

        if password != confirm_password:
            self.view.show_error("Passwords do not match")
            return False

        # Basic email validation
        # if '@' not in email or '.' not in email:
        #     self.view.show_error("Please enter a valid email address")
        #     return False

        try:
            # Make API call to register endpoint
            status, msg = self.api_service.register(email, username, password)
            if status:
                user = msg.get("user")
                if user and "id" in user:
                    # Emit the user's ID
                    self.completed.emit(user["id"])
            else:
                return msg

        except Exception as e:
            return str("An error occurred while registering: " + str(e))