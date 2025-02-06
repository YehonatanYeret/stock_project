import requests

class LoginModel:
    def __init__(self):
        self.api_url = "http://localhost:5039/api/account/signin"
        self.api_signup_url = "http://localhost:5039/api/account/signup"

    def authenticate(self, username, password):
        data = {
            "Email": username,
            "HashPassword": password
        }
        response = requests.post(self.api_url, json=data)
        return response.status_code == 200

    def signup(self, username, password):
        data = {
            "Email": username,
            "HashPassword": password
        }
        response = requests.post(self.api_signup_url, json=data)
        return (response.status_code == 200, 
                "User registered successfully!" if response.status_code == 200 
                else response.json().get("message", "Error occurred during signup."))