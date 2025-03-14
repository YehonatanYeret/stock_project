import sys
sys.path.append('C:/Users/1/source/repos/stock_project/Client')

from services.api_service import ApiService

from models.mainModels.stock_model import StockModel
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

class StockPresenter:
    """
    Presenter for handling stock-related logic
    """
    def __init__(self, stock_view, user_model, stock_model, api_service=None):
        """
        Initialize the stock presenter
        
        Args:
            stock_view: The stock view
            user_model: The user model for authentication info
            stock_model: The stock data model
            api_service: Optional API service (will create one if not provided)
        """
        self.view = stock_view
        self.user_model = user_model
        self.model = stock_model
        self.api_service = api_service if api_service else ApiService()
        
        # Connect signals from the view
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals from the stock view to handler methods"""
        self.view.search_stock_requested.connect(self.handle_search_stock)
        self.view.add_to_watchlist_requested.connect(self.handle_add_to_watchlist)
        self.view.remove_from_watchlist_requested.connect(self.handle_remove_from_watchlist)
        self.view.buy_stock_requested.connect(self.handle_buy_stock)
        self.view.refresh_data_requested.connect(self.load_available_stocks)
        self.view.view_stock_details_requested.connect(self.load_stock_details)
    
    def load_available_stocks(self):
        """Load all available stocks from the server"""
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return
        
        try:
            # Prepare headers with authentication token
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            
            # Make API call to get stocks data
            response = self.api_service.get("/stocks", headers=headers)
            
            if response.status_code == 200:
                stocks_data = response.json()
                
                # Update the model
                self.model.set_stocks(stocks_data)
                
                # Update the view
                self.view.update_stocks_list(stocks_data)
            else:
                error_message = response.json().get("message", "Failed to load stocks data")
                self.view.show_error(error_message)
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
    
    def load_stock_details(self, stock_id):
        """
        Load detailed information for a specific stock
        
        Args:
            stock_id: ID of the stock to load details for
        """
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return
        
        try:
            # Prepare headers with authentication token
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            
            # Make API call to get stock details
            response = self.api_service.get(f"/stocks/{stock_id}", headers=headers)
            
            if response.status_code == 200:
                stock_data = response.json()
                
                # Update the model with current stock
                self.model.set_current_stock(stock_data)
                
                # Update the view
                self.update_stock_detail_view(stock_data)
            else:
                error_message = response.json().get("message", "Failed to load stock details")
                self.view.show_error(error_message)
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
    
    def update_stock_detail_view(self, stock_data):
        """
        Update the stock detail view with the provided data
        
        Args:
            stock_data: Detailed stock data to display
        """
        # Update stock information in the view
        # Implementation depends on the actual view methods
        
        # Update stock chart if historical data is available
        if 'historicalData' in stock_data:
            # Extract dates and values
            dates = [item.get('date') for item in stock_data['historicalData']]
            values = [item.get('price') for item in stock_data['historicalData']]
            
            # Update chart
            self.view.update_stock_chart(dates, values)
    
    def handle_search_stock(self, query):
        """
        Search for stocks based on a query string
        
        Args:
            query: Search query (stock name or symbol)
        """
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return
        
        try:
            # Prepare headers with authentication token
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            
            # Make API call to search stocks
            params = {"q": query}
            response = self.api_service.get("/stocks", params=params, headers=headers)
            
            if response.status_code == 200:
                stocks_data = response.json()
                
                # Update the view with search results
                self.view.update_stocks_list(stocks_data)
            else:
                error_message = response.json().get("message", "Failed to search stocks")
                self.view.show_error(error_message)
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
    
    def handle_add_to_watchlist(self, stock_id):
        """
        Handle adding a stock to the watchlist
        
        Args:
            stock_id: ID of the stock to add to watchlist
        """
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return False
        
        try:
            # Prepare headers with authentication token
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            
            # Make API call to add stock to watchlist
            data = {"stockId": stock_id}
            response = self.api_service.post("/users/watchlist", data=data, headers=headers)
            
            if response.status_code in (200, 201):
                return True
            else:
                error_message = response.json().get("message", "Failed to add stock to watchlist")
                self.view.show_error(error_message)
                return False
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
            return False
    
    def handle_remove_from_watchlist(self, stock_id):
        """
        Handle removing a stock from the watchlist
        
        Args:
            stock_id: ID of the stock to remove from watchlist
        """
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return False
        
        try:
            # Prepare headers with authentication token
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            
            # Make API call to remove stock from watchlist
            response = self.api_service.delete(f"/users/watchlist/{stock_id}", headers=headers)
            
            if response.status_code in (200, 204):
                return True
            else:
                error_message = response.json().get("message", "Failed to remove stock from watchlist")
                self.view.show_error(error_message)
                return False
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
            return False
    
    def handle_buy_stock(self, stock_id, quantity, price):
        """
        Handle buying a stock
        
        Args:
            stock_id: ID of the stock to buy
            quantity: Number of shares to buy
            price: Price per share
        """
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return False
        
        # Validate inputs
        try:
            quantity = int(quantity)
            price = float(price)
            
            if quantity <= 0:
                self.view.show_error("Quantity must be positive")
                return False
            
            if price <= 0:
                self.view.show_error("Price must be positive")
                return False
        except ValueError:
            self.view.show_error("Invalid quantity or price")
            return False
        
        # Prepare transaction data
        transaction_data = {
            "stockId": stock_id,
            "quantity": quantity,
            "price": price,
            "type": "buy"
        }
        
        try:
            # Make API call to create transaction
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            response = self.api_service.post("/transactions", data=transaction_data, headers=headers)
            
            if response.status_code in (200, 201):
                return True
            else:
                error_message = response.json().get("message", "Failed to purchase stock")
                self.view.show_error(error_message)
                return False
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
            return False




class SessionManager(QObject):
    """Simple class to manage user session"""

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.session_token = None

    def get_session_info(self):
        """Get session info from server or local storage

        This is a simplified example. In a real app, you would retrieve
        this from secure storage or a session cookie.
        """
        # In a real app, this would come from your authentication system
        self.user_id = "user123"
        self.session_token = "sample_token_12345"

        return self.user_id, self.session_token


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Get session info
    session_manager = SessionManager()
    user_id, session_token = session_manager.get_session_info()

    # Create model with API base URL and session token
    api_base_url = "https://your-api-server.com"
    model = StockModel(api_base_url, session_token)
    model.set_user_id(user_id)

    # Create view
    view = StockTradingView()

    # Create presenter with model and view
    presenter = StockPresenter(model, view)

    # Show the view
    view.show()

    sys.exit(app.exec())