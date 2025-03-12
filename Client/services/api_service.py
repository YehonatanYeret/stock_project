import json
import requests
from config import API_BASE_URL, ENDPOINTS

class ApiService:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.endpoints = ENDPOINTS
        self.token = "1"
    
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
        endpoint_path = self.endpoints.get(endpoint, "")
        # Format URL with kwargs if provided (e.g., {stock_id} in the URL)
        if kwargs:
            endpoint_path = endpoint_path.format(**kwargs)
        return f"{self.base_url}{endpoint_path}"
    
    def login(self, email, password):
        """Authenticate a user with the API"""
        url = self.get_url("login")
        data = {
            "Email": email,
            "Password": password
        }
        try:
            response = requests.post(url, json=data, headers=self.get_headers())
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 400 or response.status_code == 401:
                error_data = response.json()
                return False, self._get_first_error_message(error_data, "Invalid username or password.")
            return False, "An error occurred. Please try again."
        except requests.exceptions.ConnectionError:
            return False, "Unable to connect to the server. Please check your internet connection."
        except requests.exceptions.Timeout:
            return False, "The request timed out. Please try again."
        except requests.exceptions.RequestException:
            return False, "An unexpected error occurred. Please try again."
    
    def register(self, email, username, password):
        """Register a new user with the API"""
        url = self.get_url("register")
        data = {
            "email": email,
            "username": username,
            "password": password
        }
        try:
            response = requests.post(url, json=data, headers=self.get_headers())
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 400:
                error_data = response.json()
                return False, self._get_first_error_message(error_data, "An error occurred during registration. Please try again.")
            return False, "An error occurred during registration. Please try again."
        except requests.exceptions.ConnectionError:
            return False, "Unable to connect to the server. Please check your internet connection."
        except requests.exceptions.Timeout:
            return False, "The request timed out. Please try again."
        except requests.exceptions.RequestException:
            return False, "An unexpected error occurred. Please try again."
    
    def get_user_profile(self):
        """Get the authenticated user's profile"""
        url = self.get_url("user_profile")
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get user profile error: {str(e)}")
            return {"error": str(e)}
    
    def get_portfolio(self, portfolio_id):
        """Get portfolio information"""
        url = self.get_url("portfolio")
        params = {"portfolioId": portfolio_id}
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get portfolio error: {str(e)}")
            return {"error": str(e)}
    
    def get_portfolio_performance(self, portfolio_id, days=30):
        """Get portfolio performance data for the specified number of days"""
        url = f"{self.get_url('portfolio')}/performance"
        params = {"portfolioId": portfolio_id, "days": days}
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get portfolio performance error: {str(e)}")
            return {"error": str(e)}
    
    def get_portfolio_holdings(self, portfolio_id):
        """Get holdings in the portfolio"""
        url = f"{self.get_url('portfolio')}/holdings"
        params = {"portfolioId": portfolio_id}
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get portfolio holdings error: {str(e)}")
            return {"error": str(e)}
    
    def get_stocks(self):
        """Get list of available stocks"""
        url = self.get_url("stocks")
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get stocks error: {str(e)}")
            return {"error": str(e)}
    
    def get_stock_details(self, stock_id):
        """Get detailed information about a specific stock"""
        url = self.get_url("stock_details", stock_id=stock_id)
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get stock details error: {str(e)}")
            return {"error": str(e)}
    
    def get_stock_performance(self, stock_id, days=30):
        """Get performance data for a specific stock"""
        url = f"{self.get_url('stock_details', stock_id=stock_id)}/performance"
        params = {"days": days}
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get stock performance error: {str(e)}")
            return {"error": str(e)}
    
    def get_transactions(self, portfolio_id=None):
        """Get transaction history, optionally filtered by portfolio"""
        url = self.get_url("transactions")
        params = {}
        if portfolio_id:
            params["portfolioId"] = portfolio_id
        try:
            response = requests.get(url, params=params, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get transactions error: {str(e)}")
            return {"error": str(e)}
    
    def execute_transaction(self, transaction_data):
        """Execute a buy/sell transaction"""
        url = self.get_url("transactions")
        try:
            response = requests.post(url, json=transaction_data, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Execute transaction error: {str(e)}")
            return {"error": str(e)}

    def _get_first_error_message(self, error_data, default_message):
        """
        Helper function to extract the first error message from the validation errors.
        """
        if 'errors' in error_data:
            validation_errors = error_data['errors']
            for field, errors in validation_errors.items():
                return errors[0]  # Return the first error for the first field
        return default_message