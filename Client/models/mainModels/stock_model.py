from PySide6.QtCore import QObject, Signal

class StockModel:
    def __init__(self):
        self._stocks = []
        self._current_stock = None
        self._observers = []
    
    def register_observer(self, observer):
        """Add an observer to be notified of model changes"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self):
        """Notify all observers of a change in the model"""
        for observer in self._observers:
            observer.model_updated()
    
    def set_stocks(self, stocks):
        """Set the list of stocks"""
        self._stocks = stocks
        self.notify_observers()
    
    def set_current_stock(self, stock):
        """Set the currently selected stock"""
        self._current_stock = stock
        self.notify_observers()
    
    def get_stocks(self):
        """Get all stocks"""
        return self._stocks
    
    def get_stock(self, stock_id):
        """Get a specific stock by ID"""
        for stock in self._stocks:
            if stock['id'] == stock_id:
                return stock
        return None

class StockModel(QObject):
    """Model class for handling stock data and API interactions"""

    # Signals
    stock_data_updated = Signal(dict)
    transaction_completed = Signal(str, bool)
    error_occurred = Signal(str)

    def __init__(self, api_base_url, session_token=None):
        super().__init__()
        self.api_base_url = api_base_url
        self.session_token = session_token
        self.user_id = None
        self._current_stock = None

    def set_user_id(self, user_id):
        """Set the current user ID from session"""
        self.user_id = user_id

    def get_stock_data(self, symbol, start_date, end_date):
        """Get stock data from API

        Args:
            symbol (str): Stock symbol
            start_date (QDate): Start date
            end_date (QDate): End date
        """
        try:
            # Convert QDate to standard date format
            start_str = start_date.toString("yyyy-MM-dd")
            end_str = end_date.toString("yyyy-MM-dd")

            # Construct API endpoint
            endpoint = f"{self.api_base_url}/api/stocks/{symbol}"

            # Create request parameters
            params = {
                "startDate": start_str,
                "endDate": end_str
            }

            # Add authorization headers
            headers = {"Authorization": f"Bearer {self.session_token}"}

            # Make API request
            response = requests.get(endpoint, params=params, headers=headers)

            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                self.current_stock = data
                self.stock_data_updated.emit(data)
                return data
            else:
                error_message = f"Error fetching stock data: {response.status_code}"
                self.error_occurred.emit(error_message)
                return None

        except Exception as e:
            error_message = f"Error fetching stock data: {str(e)}"
            self.error_occurred.emit(error_message)
            return None

    def execute_transaction(self, transaction_type, symbol, quantity, price):
        """Execute a buy or sell transaction

        Args:
            transaction_type (str): "buy" or "sell"
            symbol (str): Stock symbol
            quantity (int): Number of shares
            price (float): Price per share
        """
        if not self.user_id:
            self.error_occurred.emit("User not authenticated")
            return False

        try:
            # Construct API endpoint
            endpoint = f"{self.api_base_url}/api/transactions"

            # Create transaction data
            transaction_data = {
                "userId": self.user_id,
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "type": transaction_type,
                "timestamp": datetime.now().isoformat()
            }

            # Add authorization headers
            headers = {
                "Authorization": f"Bearer {self.session_token}",
                "Content-Type": "application/json"
            }

            # Make API request
            response = requests.post(endpoint, json=transaction_data, headers=headers)

            # Check if request was successful
            if response.status_code == 200 or response.status_code == 201:
                result_data = response.json()
                success_message = f"Successfully {transaction_type}ed {quantity} shares of {symbol}"
                self.transaction_completed.emit(success_message, True)
                return True
            else:
                error_message = f"Transaction failed: {response.status_code}"
                self.error_occurred.emit(error_message)
                return False

        except Exception as e:
            error_message = f"Transaction error: {str(e)}"
            self.error_occurred.emit(error_message)
            return False

    def get_user_portfolio(self):
        """Get the user's current portfolio"""
        if not self.user_id:
            self.error_occurred.emit("User not authenticated")
            return None

        try:
            # Construct API endpoint
            endpoint = f"{self.api_base_url}/api/portfolio/{self.user_id}"

            # Add authorization headers
            headers = {"Authorization": f"Bearer {self.session_token}"}

            # Make API request
            response = requests.get(endpoint, headers=headers)

            # Check if request was successful
            if response.status_code == 200:
                return response.json()
            else:
                error_message = f"Error fetching portfolio: {response.status_code}"
                self.error_occurred.emit(error_message)
                return None

        except Exception as e:
            error_message = f"Error fetching portfolio: {str(e)}"
            self.error_occurred.emit(error_message)
            return None
        for stock in self._stocks:
            if stock['id'] == stock_id:
                return stock
        return None
    
    @property
    def current_stock(self):
        return self._current_stock