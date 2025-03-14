import datetime

from PySide6.QtCore import QDate
from services.api_service import ApiService


class StockModel:
    """Model for stock data and trading operations"""

    def __init__(self, api_service=None):
        """Initialize the model with an API service
        
        Args:
            api_service: Service for API communication, creates a new one if not provided
        """
        self.api_service = api_service or ApiService()
        self.current_user_id = None
        self.current_stock = None

    def set_user(self, user_id, token=None):
        """Set the current user and authentication token
        
        Args:
            user_id: ID of the current user
            token: Authentication token for API requests
        """
        self.current_user_id = user_id
        if token:
            self.api_service.set_token(token)

    def fetch_stock_data(self, symbol, start_date, end_date):
        """Fetch stock data for a given symbol and date range
        
        Args:
            symbol: Stock symbol (e.g., AAPL)
            start_date: Start date for historical data
            end_date: End date for historical data
            
        Returns:
            (success, data): Tuple with success flag and stock data or error
        """

        # Convert QDate to datetime.date if necessary
        def convert_to_date(date_obj):
            if isinstance(date_obj, QDate):
                return date_obj.toPython()  # Converts QDate to Python's datetime.date
            return date_obj

        start_date = convert_to_date(start_date)
        end_date = convert_to_date(end_date)

        start_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime.date) else start_date
        end_str = end_date.strftime("%Y-%m-%d") if isinstance(end_date, datetime.date) else end_date

        success, response = self.api_service.get("stock_details", params={
            "ticker": symbol,
            "startDate": start_str,
            "endDate": end_str
        })

        if success:
            self.current_stock = response

        return success, response

    def execute_buy_order(self, symbol, quantity, price):
        """Execute a buy order
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to buy
            price: Price per share
            
        Returns:
            (success, data): Tuple with success flag and transaction data or error
        """
        if not self.current_user_id:
            return False, {"error": "No user is logged in"}

        order_data = {
            "user_id": self.current_user_id,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "type": "buy",
            "timestamp": datetime.datetime.now().isoformat()
        }

        return self.api_service.post("orders", order_data)

    def execute_sell_order(self, symbol, quantity, price):
        """Execute a sell order
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to sell
            price: Price per share
            
        Returns:
            (success, data): Tuple with success flag and transaction data or error
        """
        if not self.current_user_id:
            return False, {"error": "No user is logged in"}

        # Check if user has enough shares to sell
        for holding in self.user_holdings:
            if holding["symbol"] == symbol and holding["quantity"] >= quantity:
                order_data = {
                    "user_id": self.current_user_id,
                    "symbol": symbol,
                    "quantity": quantity,
                    "price": price,
                    "type": "sell",
                    "timestamp": datetime.datetime.now().isoformat()
                }

                return self.api_service.post("orders", order_data)

        return False, {"error": f"Insufficient shares of {symbol} to sell"}
