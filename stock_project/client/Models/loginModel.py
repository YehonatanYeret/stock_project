#שיעורי בית להעביר לכאן את בדיקת האימות

class LoginModel:
    def __init__(self):
        self.users = {"admin": "password"}
    def authenticate(self, username, password):
        return username in self.users and self.users[username] == password
