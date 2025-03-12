from services.api_service import ApiService

class PortfolioPresenter:
    """
    Presenter for handling portfolio management logic
    """
    def __init__(self, portfolio_view, user_model, portfolio_model, api_service=None):
        """
        Initialize the portfolio presenter
        
        Args:
            portfolio_view: The portfolio view
            user_model: The user model for authentication info
            portfolio_model: The portfolio data model
            api_service: Optional API service (will create one if not provided)
        """
        self.view = portfolio_view
        self.user_model = user_model
        self.model = portfolio_model
        self.api_service = api_service if api_service else ApiService()
        
        # Connect signals from the view
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals from the portfolio view to handler methods"""
        self.view.add_stock_requested.connect(self.handle_add_stock)
        self.view.remove_stock_requested.connect(self.handle_remove_stock)
        self.view.refresh_data_requested.connect(self.load_portfolio_data)
    
    def load_portfolio_data(self):
        """Load the user's portfolio data from the server"""
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return
        
        try:
            # Prepare headers with authentication token
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            
            # Make API call to get portfolio data
            response = self.api_service.get("/portfolio", headers=headers)
            
            if response.status_code == 200:
                portfolio_data = response.json()
                
                # Update the portfolio model
                self.model.set_portfolio_data(portfolio_data)
                
                # Update the view with portfolio data
                self.update_portfolio_view()
            else:
                error_message = response.json().get("message", "Failed to load portfolio data")
                self.view.show_error(error_message)
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
    
    def update_portfolio_view(self):
        """Update the portfolio view with current model data"""
        # Get data from the model
        portfolio_summary = self.model.get_summary()
        holdings = self.model.get_holdings()
        allocations = self.model.get_allocations()
        performance_data = self.model.get_performance_data()
        
        # Update the view components
        self.view.update_portfolio_summary(
            portfolio_summary.get('total_value', 0),
            portfolio_summary.get('total_gain', 0),
            portfolio_summary.get('gain_percentage', 0)
        )
        self.view.update_allocation_chart(allocations)
        self.view.update_holdings_table(holdings)
        self.view.update_performance_chart(
            performance_data.get('dates', []),
            performance_data.get('values', [])
        )
    
    def handle_add_stock(self, stock_id, quantity, price):
        """
        Handle adding a stock to the portfolio
        
        Args:
            stock_id: ID of the stock to add
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
                # Refresh portfolio data
                self.load_portfolio_data()
                return True
            else:
                error_message = response.json().get("message", "Failed to add stock")
                self.view.show_error(error_message)
                return False
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
            return False
    
    def handle_remove_stock(self, stock_id):
        """
        Handle removing a stock from the portfolio (selling all shares)
        
        Args:
            stock_id: ID of the stock to remove
        """
        if not self.user_model.is_authenticated:
            self.view.show_error("User not authenticated")
            return False
        
        # Get current holding for this stock
        holding = self.model.get_holding_by_id(stock_id)
        
        if not holding:
            self.view.show_error("Stock not found in portfolio")
            return False
        
        quantity = holding.get('quantity', 0)
        current_price = holding.get('current_price', 0)
        
        if quantity <= 0:
            self.view.show_error("No shares to sell")
            return False
        
        # Prepare transaction data
        transaction_data = {
            "stockId": stock_id,
            "quantity": quantity,
            "price": current_price,
            "type": "sell"
        }
        
        try:
            # Make API call to create transaction
            headers = {"Authorization": f"Bearer {self.user_model.token}"}
            response = self.api_service.post("/transactions", data=transaction_data, headers=headers)
            
            if response.status_code in (200, 201):
                # Refresh portfolio data
                self.load_portfolio_data()
                return True
            else:
                error_message = response.json().get("message", "Failed to remove stock")
                self.view.show_error(error_message)
                return False
                
        except Exception as e:
            self.view.show_error(f"Connection error: {str(e)}")
            return False
    
    def handle_period_change(self, period_index):
        """
        Handle when the user changes the time period for performance chart
        
        Args:
            period_index: Index of the selected period (e.g., 0 for 1W, 1 for 1M, etc.)
        """
        # Map period index to actual period
        periods = ["1W", "1M", "3M", "6M", "1Y", "All"]
        selected_period = periods[period_index] if 0 <= period_index < len(periods) else "1M"
        
        # Update the performance chart with data for the selected period
        performance_data = self.model.get_performance_data(selected_period)
        
        self.view.update_performance_chart(
            performance_data.get('dates', []),
            performance_data.get('values', [])
        )