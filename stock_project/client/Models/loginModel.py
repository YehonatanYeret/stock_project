# Models/loginModel.py

class LoginModel:
    def __init__(self):
        # For demo purposes we start with one default user.
        self.users = {"admin": "password"}
    
    def authenticate(self, username, password):
        """
        Check if the provided username and password are valid.
        """
        return username in self.users and self.users[username] == password
    
    def signup(self, username, password):
        """
        Perform basic validation for signup.
        Returns a tuple: (success: bool, message: str)
        """
        if username in self.users:
            return False, "Username already exists."
        if len(password) < 4:
            return False, "Password must be at least 4 characters long."
        # For demo purposes, add the new user.
        self.users[username] = password
        return True, "Sign up successful!" + username + password
