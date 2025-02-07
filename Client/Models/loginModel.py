import requests

class LoginModel:
    def __init__(self):
        self.api_url = "http://localhost:5039/api/account/signin"
        self.api_signup_url = "http://localhost:5039/api/account/signup"

    def authenticate(self, username, password):
        data = {
            "email": username,
            "hashPassword": password
        }
        try:
            response = requests.post(self.api_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return True, result.get("userId", None), "User logged in successfully."
            elif response.status_code == 400 or response.status_code == 401:
                error_data = response.json()
                return False, None, error_data.get("message", "An error occurred. Please try again.")
            else:
                return False, None, "An error occurred. Please try again."
                
        except requests.exceptions.ConnectionError:
            return False, None, "Unable to connect to the server. Please check your internet connection."
        except requests.exceptions.Timeout:
            return False, None, "The request timed out. Please try again."
        except requests.exceptions.RequestException:
            return False, None, "An unexpected error occurred. Please try again."

    def signup(self, username, password):
        data = {
            "email": username,
            "hashPassword": password
        }
        try:
            response = requests.post(self.api_signup_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return True, result.get("userId", None), "User registered successfully!"
            elif response.status_code == 400:
                error_data = response.json()
                return False, None, error_data.get("message", "An error occurred during signup. Please try again.")
            else:
                return False, None, "An error occurred during signup. Please try again."
                
        except requests.exceptions.ConnectionError:
            return False, None, "Unable to connect to the server. Please check your internet connection."
        except requests.exceptions.Timeout:
            return False, None, "The request timed out. Please try again."
        except requests.exceptions.RequestException:
            return False, None, "An unexpected error occurred. Please try again."