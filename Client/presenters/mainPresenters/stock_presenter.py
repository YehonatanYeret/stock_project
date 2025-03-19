import datetime
import json

from PySide6.QtCore import QDate
from PySide6.QtCore import QObject, Slot, QDate

class StockPresenter(QObject):
    """Presenter for stock trading application, connects model and view"""

    def __init__(self, model, view, user_id=None):
        """Initialize the presenter with model and view
        
        Args:
            model: The stock model instance
            view: The stock view instance
            user_id: Optional user ID for automatic login
        """
        super().__init__()
        self.model = model
        self.view = view

        # Connect view signals to presenter slots
        self._connect_signals()

        # Load user data if provided
        if user_id:
            self.model.set_user(user_id)

    def _connect_signals(self):
        """Connect signals from view to presenter slots"""
        # Search functionality
        self.view.search_stock_requested.connect(self.on_search_stock)

        # Trading functionality
        self.view.buy_stock_requested.connect(self.on_buy_stock)
        self.view.sell_stock_requested.connect(self.on_sell_stock)

    @Slot(str, QDate, QDate)
    def on_search_stock(self, symbol, start_date, end_date):
        """Handle stock search request from view
        
        Args:
            symbol: Stock symbol to search for
            start_date: Start date for historical data
            end_date: End date for historical data
        """
        if not symbol:
            self.view.show_message("Please enter a stock symbol", True)
            return

        # Validate date range
        if start_date > end_date:
            self.view.show_message("Start date must be before end date", True)
            return

        # Don't allow searches for future dates
        today = QDate.currentDate()
        if end_date > today:
            end_date = today
            self.view.show_message("End date adjusted to today", False)

        # Fetch stock data from model
        success, stock_data = self.model.fetch_stock_data(symbol, start_date, end_date)

        if success:
            # Format data for view if needed
            formatted_data = self._format_stock_data(symbol, stock_data)
            # Update view with the data
            # Convert QDate to datetime.date if necessary
            def convert_to_date(date_obj):
                if isinstance(date_obj, QDate):
                    return date_obj.toPython()  # Converts QDate to Python's datetime.date
                return date_obj

            start_date = convert_to_date(start_date)
            end_date = convert_to_date(end_date)

            start_str = start_date.strftime("%Y-%m-%d") if isinstance(start_date, datetime.date) else start_date
            end_str = end_date.strftime("%Y-%m-%d") if isinstance(end_date, datetime.date) else end_date
            self.view.update_stock_data(symbol, start_str, end_str, formatted_data)
        else:
            error_msg = stock_data.get("error", f"Failed to retrieve data for {symbol}")
            self.view.show_message(error_msg, True)

    @Slot(str, int)
    def on_buy_stock(self, symbol, quantity):
        """Handle buy stock request from view
        
        Args:
            symbol: Stock symbol to buy
            quantity: Number of shares to buy
            price: Price per share
        """
        # Execute sell order through model
        success, result = self.model.execute_buy_order(symbol, quantity)

        if success:
            self.view.show_message(f"Successfully bought {quantity} shares of {symbol}!")
        else:
            self.view.show_message(result, True)

    @Slot(str, float)
    def on_sell_stock(self, symbol, quantity):
        """Handle sell stock request from view
        
        Args:
            symbol: Stock symbol to sell
            quantity: Number of shares to sell
            price: Price per share
        """

        # Execute sell order through model
        success, result = self.model.execute_sell_order(symbol, quantity)

        if success:
            self.view.show_message(f"Successfully sold {quantity} shares of {symbol}!")
        else:
            self.view.show_message(result, True)

    def _format_stock_data(self, symbol, api_data):
            """Format API data for display in the view
            
            Args:
                symbol: Stock symbol
                api_data: Raw data from API
                
            Returns:
                dict: Formatted data for view consumption
            """
            try:
                print(api_data)
                aggregate_data = json.loads(api_data.get("aggregateData", "{}"))
                return {
                    "name": api_data.get("name", "Unknown Company"),
                    "symbol": symbol,
                    "description": api_data.get("description", "No description available"),
                    "chart_data": aggregate_data.get("results", []),  # Default to empty list
                    "img": api_data.get("logoBase64", None),
                    "price": api_data.get("sellPrice", 0),
                }

            except Exception as e:
                print(f"Error formatting stock data: {str(e)}")

                # Return fallback data if formatting fails
                return {
                    "name": f"{symbol} Inc.",
                    "symbol": symbol,
                    "description": "No description available",
                    "volume": 0,
                    "chart_data": {},
                    "img": None,
                    "price": 0,
                }