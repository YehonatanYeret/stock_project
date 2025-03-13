import json
import requests
from config import API_BASE_URL, ENDPOINTS


class ApiService:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.endpoints = ENDPOINTS
        self.token = None  # Default to None until set

    def set_token(self, token):
        """Set the authentication token for API requests"""
        self.token = token

    def get_headers(self):
        """Get headers for API requests, including authentication token if available"""
        headers = {
            'Content-Type': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def get_url(self, endpoint, **kwargs):
        """Get the full URL for an endpoint, with optional format arguments"""
        if endpoint not in self.endpoints:
            raise ValueError(f"Unknown API endpoint: {endpoint}")
        
        endpoint_path = self.endpoints[endpoint]
        if kwargs:
            endpoint_path = endpoint_path.format(**kwargs)
        return f"{self.base_url}{endpoint_path}"

    def login(self, email, password):
        """Authenticate a user with the API"""
        return self.post("login", {"Email": email, "Password": password})

    def register(self, email, username, password):
        """Register a new user with the API"""
        return self.post("register", {"email": email, "username": username, "password": password})
    
    def get_holdings(self, user_id):
        """Fetch holdings for a user"""
        return self.get("holdings", user_id=user_id)
    
    def get_transactions(self, user_id):
        """Fetch transactions for a user"""
        return self.get("transactions", user_id=user_id)


    def get(self, endpoint, params=None, **kwargs):
        """Generic GET request handler"""
        url = self.get_url(endpoint, **kwargs)
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET {url} failed: {str(e)}")
            return False, {"error": str(e)}
        except json.JSONDecodeError:
            return False, {"error": "Invalid JSON response from server"}

    def post(self, endpoint, data, **kwargs):
        """Generic POST request handler"""
        url = self.get_url(endpoint, **kwargs)
        try:
            response = requests.post(url, json=data, headers=self.get_headers())
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            print(f"POST {url} failed: {str(e)}")
            return False, {"error": str(e)}
        except json.JSONDecodeError:
            return False, {"error": "Invalid JSON response from server"}



    def _get_first_error_message(self, error_data, default_message):
        """Extract the first error message from validation errors."""
        if 'errors' in error_data:
            for field, errors in error_data['errors'].items():
                return errors[0]  # Return first error message
        return default_message
