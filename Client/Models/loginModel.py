import requests

api_url = 'http://localhost:5039/api/auth'

class LoginModel:
    def __init__(self):
        self.api_signin_url = f"{api_url}/query/signin"
        self.api_signup_url = f"{api_url}/command/signup"

    def authenticate(self, username, password):
        data = {
            "email": username,
            "name": "",
            "hashPassword": password
        }

        # Send request to server
        try:
            response = requests.post(self.api_signin_url, json=data)

            # Check response status code
            if response.status_code == 200:
                result = response.json()

                # Return success message and user ID
                return True, result.get("userId", None), "User logged in successfully."
            elif response.status_code == 400 or response.status_code == 401:
                error_data = response.json()

                # Extract the first error from the validation errors
                first_error_message = self._get_first_error_message(error_data, "Invalid username or password.")
                return False, None, first_error_message
            else:
                return False, None, "An error occurred. Please try again."

        except requests.exceptions.ConnectionError:
            return False, None, "Unable to connect to the server. Please check your internet connection."
        except requests.exceptions.Timeout:
            return False, None, "The request timed out. Please try again."
        except requests.exceptions.RequestException:
            return False, None, "An unexpected error occurred. Please try again."

    def signup(self, email, username, password):
        # Validate password before sending request
        if len(password) < 6:
            return False, None, "Password must be at least 6 characters long."

        if len(username) < 4:
            return False, None, "Username must be at least 4 characters long."
        if username.isnumeric():
            return False, None, "Username cannot be all numbers."

        data = {
            "email": email,
            "name": username,
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
                
                # Extract the first error from the validation errors
                first_error_message = self._get_first_error_message(error_data, "An error occurred during signup. Please try again.")
                return False, None, first_error_message
            else:
                return False, None, "An error occurred during signup. Please try again."

        except requests.exceptions.ConnectionError:
            return False, None, "Unable to connect to the server. Please check your internet connection."
        except requests.exceptions.Timeout:
            return False, None, "The request timed out. Please try again."
        except requests.exceptions.RequestException:
            return False, None, "An unexpected error occurred. Please try again."

    def _get_first_error_message(self, error_data, default_message):
        """
        Helper function to extract the first error message from the validation errors.
        """
        if 'errors' in error_data:
            validation_errors = error_data['errors']
            for field, errors in validation_errors.items():
                return errors[0]  # Return the first error for the first field
        return default_message