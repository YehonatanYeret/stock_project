import requests
api_url = 'http://localhost:5039/api/transaction'

class StockModel:
    def __init__(self):
        pass
        # Validate email address before sending request
        if '@' not in username or '.' not in username or len(username) < 5:
            return False, None, "Invalid email address. Please enter a valid email address."

        # Validate password before sending request
        if len(password) < 6:
            return False, None, "Password must be at least 6 characters long."

        data = {
            "email": username,
            "hashPassword": password
        }

        # Send request to server
        try:
            response = requests.post(self.api_signup_url, json=data)
            
            # Check response status code
            if response.status_code == 200:
                result = response.json()

                # Return success message and user ID
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