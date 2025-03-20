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
        success, response = self.post("signin", {"Email": email, "Password": password})
        if success:
            return True, response
        else:
            return False, self._extract_backend_message(response, "Login failed. Please try again.")

    def register(self, email, username, password):
        """Register a new user with the API"""
        success, response = self.post("signup", {"Email": email, "Name": username, "Password": password})
        if success:
            return True, response
        else:
            return False, self._extract_backend_message(response, "Registration failed. Please try again.")

    def get_holdings(self, user_id):
        """Fetch holdings for a user"""
        return self.get("holdings", user_id=user_id)
    
    def get_transactions(self, user_id):
        """Fetch transactions for a user"""
        return self.get("transactions", user_id=user_id)

    def get_cash_balance(self, user_id):
        """Fetch cash balance for a user"""
        success, response = self.get("cash_balance", user_id=user_id)
        if success:
            return float(response)
        print(f"Failed to fetch cash balance: {response}")
        return 0.00

    def get_profit(self, user_id):
        """Fetch total profit for a user"""
        success, response = self.get("profit", user_id=user_id)
        if success:
            return float(response)
        print(f"Failed to fetch total profit: {response}")
        return 0.00

    def add_money(self, user_id, amount):
        """Add money to a user's account"""
        success, response = self.post("deposit_money", {"userId": user_id, "amount": amount})
        if success:
            return float(response)

    def remove_money(self, user_id, amount):
        """Remove money from a user's account"""
        success, response = self.post("withdraw_money", {"userId": user_id, "amount": amount})
        if success:
            return float(response)

    def sell_stock(self, user_id, symbol, quantity):
        """
        Sell a stock holding using the correct API endpoint format.
        The endpoint is defined as:
          "sell_stock": "/transaction/command/sell/{user_id}"
        Here, we pass the parameters as keyword arguments so that they get inserted into the URL.
        """
        # Passing an empty dictionary as the payload because all necessary data is provided in the URL.
        success, response = self.post("sell_stock", data={"ticker":str(symbol), "quantity":float(quantity)}, user_id=user_id)
        if success:
            return True, response
        else:
            return False, self._extract_backend_message(response, "Failed to sell stock. Please try again.")

    def buy_stock(self, user_id, symbol, quantity):
        success, response = self.post("buy_stock", data={"ticker":str(symbol), "quantity":float(quantity)}, user_id=user_id)
        if success:
            return True, response
        else:
            print("bad request")
            return False, self._extract_backend_message(response, "Failed to buy stock. Please try again.")

    def search_stock(self, symbol, startDate, endDate):
        seccess, response = self.get("stock_details", params={
                "ticker": symbol,
                "startDate": startDate,
                "endDate": endDate
            })
        if seccess:
            return True, response
        else:
            return False, self._extract_backend_message(response, "Failed to search stock. Please try again.")

    def get_AI_response(self, message):

        # # Process the PDF before querying the model
        # url = "http://localhost:5039/api/AI/query/process-pdf"
        # requests.post(url)

        success, response = self.get("ai_response", params={"query": message})
        if success:
            return True, response["response"]
        else:
            return False, self._extract_backend_message(response, "Failed to get AI response. Please try again.")

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
        except Exception as e:
            return False, {"error": str(e)}

    def post(self, endpoint, data, **kwargs):
        """Generic POST request handler"""
        url = self.get_url(endpoint, **kwargs)
        try:
            response = requests.post(url, json=data, headers=self.get_headers())
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.HTTPError as http_err:
            try:
                error_data = response.json() if response.content else {}
            except json.JSONDecodeError:
                error_data = {"message": "Invalid response from server."}
            return False, error_data
        except requests.exceptions.RequestException as e:
            print(f"POST {url} failed: {str(e)}")
            return False, {"error": str(e)}
        except json.JSONDecodeError:
            return False, {"error": "Invalid JSON response from server"}
        except Exception as e:
            return False, {"error": str(e)}

    def _extract_backend_message(self, response, default_message):
        """
        Extract meaningful error messages from the backend response.
        - Looks for a "message" field first.
        - If validation errors exist, it extracts the first one.
        - Otherwise, it falls back to a default message.
        """
        print(response)
        if isinstance(response, dict):
            if "message" in response:
                return response["message"]
            elif "errors" in response:
                for _, errors in response["errors"].items():
                    return errors[0]
        return default_message

    def process_pdf(self):
        """Process the PDF through the API"""
        success, response = self.post("process_pdf", data={})
        if success:
            return True, response
        else:
            return False, self._extract_backend_message(response, "Failed to process PDF. Please try again.")
