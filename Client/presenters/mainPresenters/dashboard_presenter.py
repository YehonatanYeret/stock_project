from PySide6.QtCore import QObject

class StockPresenter(QObject):
    """Presenter class for managing interactions between Model and View"""

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        """Connect signals and slots between model, view, and presenter"""
        # Connect view signals to presenter methods
        self.view.search_stock_requested.connect(self.on_search_stock)
        self.view.buy_stock_requested.connect(self.on_buy_stock)
        self.view.sell_stock_requested.connect(self.on_sell_stock)

        # Connect model signals to presenter methods
        self.model.stock_data_updated.connect(self.on_stock_data_updated)
        self.model.transaction_completed.connect(self.on_transaction_completed)
        self.model.error_occurred.connect(self.on_error)

    def on_search_stock(self, symbol, start_date, end_date):
        """Handle stock search request from view"""
        # Validate input
        if not symbol:
            self.view.show_message("Please enter a stock symbol", is_error=True)
            return

        if start_date > end_date:
            self.view.show_message("Start date must be before end date", is_error=True)
            return

        # Request data from model
        self.model.get_stock_data(symbol, start_date, end_date)

    def on_buy_stock(self, symbol, quantity, price):
        """Handle buy stock request from view"""
        # Validate input
        if not symbol:
            self.view.show_message("Please enter a stock symbol", is_error=True)
            return

        if quantity <= 0:
            self.view.show_message("Quantity must be greater than zero", is_error=True)
            return

        # Execute transaction through model
        self.model.execute_transaction("buy", symbol, quantity, price)

    def on_sell_stock(self, symbol, quantity, price):
        """Handle sell stock request from view"""
        # Validate input
        if not symbol:
            self.view.show_message("Please enter a stock symbol", is_error=True)
            return

        if quantity <= 0:
            self.view.show_message("Quantity must be greater than zero", is_error=True)
            return

        # Check if user has enough shares in portfolio
        portfolio = self.model.get_user_portfolio()
        if portfolio:
            user_shares = 0
            for position in portfolio.get("positions", []):
                if position["symbol"] == symbol:
                    user_shares = position["quantity"]
                    break

            if user_shares < quantity:
                self.view.show_message(f"You only have {user_shares} shares of {symbol}", is_error=True)
                return

        # Execute transaction through model
        self.model.execute_transaction("sell", symbol, quantity, price)

    def on_stock_data_updated(self, stock_data):
        """Handle stock data updates from model"""
        # Format data for view if needed
        formatted_data = self._format_stock_data(stock_data)

        # Update view with formatted data
        self.view.update_stock_data(formatted_data)

    def on_transaction_completed(self, message, success):
        """Handle transaction completion from model"""
        # Show success message
        self.view.show_message(message, is_error=not success)

        # Refresh portfolio data if available
        portfolio = self.model.get_user_portfolio()
        if portfolio and hasattr(self.view, 'update_portfolio'):
            self.view.update_portfolio(portfolio)

    def on_error(self, error_message):
        """Handle errors from model"""
        self.view.show_message(error_message, is_error=True)

    def _format_stock_data(self, api_data):
        """Format raw API data for the view

        This converts the ASP.NET API response format to the format expected by the view
        """
        # Example transformation (adjust based on your actual API response)
        formatted_data = {
            "name": api_data.get("companyName", "Unknown Company"),
            "symbol": api_data.get("symbol", ""),
            "price": api_data.get("currentPrice", 0.0),
            "change_pct": api_data.get("changePercentage", 0.0),
            "volume": api_data.get("volume", 0),
            "market_cap": api_data.get("marketCap", 0.0) / 1_000_000_000,  # Convert to billions
            "stats": {
                "52_week_high": api_data.get("fiftyTwoWeekHigh", 0.0),
                "52_week_low": api_data.get("fiftyTwoWeekLow", 0.0),
                "avg_volume": api_data.get("averageVolume", 0),
                "pe_ratio": api_data.get("peRatio", 0.0),
                "beta": api_data.get("beta", 0.0),
                "dividend": api_data.get("dividendYield", 0.0) * 100  # Convert to percentage
            }
        }

        # Format chart data
        if "historicalData" in api_data:
            chart_data = []
            for point in api_data["historicalData"]:
                chart_data.append({
                    "date": point.get("date", ""),
                    "open": point.get("open", 0.0),
                    "high": point.get("high", 0.0),
                    "low": point.get("low", 0.0),
                    "close": point.get("close", 0.0),
                    "volume": point.get("volume", 0)
                })
            formatted_data["chart_data"] = chart_data

        return formatted_data



import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject

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