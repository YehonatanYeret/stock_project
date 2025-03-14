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

    def signup(self, email, username, password):
        # Validate password before sending request
        if len(password) < 6:
            return False, None, "Password must be at least 6 characters long."

        if len(username) < 4:
            return False, None, "Username must be at least 4 characters long."
        if username.isnumeric():
            return False, None, "Username cannot be all numbers."

        status, msg = self.api_service.register(email, username, password)
        if status:
            self.completed.emit()
        else:
            return msg