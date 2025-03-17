import datetime
import json

from PySide6.QtCore import QDate
from PySide6.QtCore import QObject, Slot, QDate

DEFAULT_ICON = "iVBORw0KGgoAAAANSUhEUgAAARMAAAC3CAMAAAAGjUrGAAAAclBMVEX///8AAAB1dXXi4uImJibFxcVgYGDo6OgcHBz29vaysrKWlpbQ0NBoaGgZGRkICAjb29uFhYW3t7c7OzvIyMhPT0++vr6NjY0jIyNISEiioqJUVFTx8fHNzc3d3d1JSUmenp55eXkxMTFkZGQ/Pz8TExMsgbRjAAAEp0lEQVR4nO2d63bqIBBGQ423qvWurdpWbX3/VzxtgFxgSKKnCcp8+5cLqAv2ashAmBhFAAAAAAAAAAAAAAAAAAAAAFTyPl8PSnndjz58d7JVurGow7rju6PtMa9l5JeF7662xVNtJUI8++5sOzxfoUQIFpfP8Col4tN3f9tgp0c77U3c7FMpM98dboE3NdZjebOhnnW2bXTKM7Unzyc2F09fjvStRlPZ8tx4l7yjnOxqNO0lLePGu+Sdft1LR188cJKHq5POZGmyHao6pk7GVJg2VVKYOjmTsetcVvJ0ciCViG/ZlKeTiHayl5VMnZxIJ2rXhKmTaE8o0Sscrk6i2cKkr6vYOikBTmzgxAZObODEBk5s2DpZPZukm9JMnQz1jnWek2rK1MmEUJJWMnVCKhFrWcnTieOZIO+9giXpRC0CmTr5oJRoC0ydRP352mB/1E25OilD3pSmjXfJO1c4ma3ef2m8S965wgkb4MQGTmzgxAZObCgnw2vx1fmGIJx06FWPm4G33jfDXzgJLbSFExs4seHthM6p4O2ETr9xO3kaVXJcPrqT9BBWHreTVY3v/Hp8J0S86nbSrfGdj36MWI50aeRVwEkyTxRC8Q6cJBzzxc9wIgeRnz+HczhJ6PVzNZ3PMicb+6FP+tdBOTHytRb5gK7ohE6hPMjKEJxMFclnV7Jw0QmpREc6ATjRGx0q1eCNzrYvOHEcN1d5YQE4eVEf0/SLE7VFVuf/ZCIrQ3RCJr0VndCJ+yryC9OJOI/NhsZ9h0rd36i6QJ0I8XUoNjTjk+HMIJuGgnUixKjQkFfM5nIiXvICeDm5jCVEHJbbcOLlpJR0wwlOcqhFD5zkkUs7OKl0MtzNTXR4wtVJn2rYU98ZgJPLSrLLRvcylkUjl5Nv0p6aegJwQsQneqncdThxHK1WKcdhO9nASW0nEZW9wuTacToJfY69xQl1L05DF65OygjAibEfm3fiuu+UE4ATEb8mDHJTQ76IpZMK4ARO4ITgZieH2bhIUHvU0ydJL9MwPcmivdMJ9SxDP1YNwIm+8c6y0emilcsJw2delTEbfZUF/Wy0ygm/Z+g3/5+Ec9biFiehn8m5aQ24WaZHeTRfAZ3dwhrQ4Kfz060kF3JcRrJowtVJFXACJ3BCACc2cGIjbrwXv+/N8GRw0ifgAnByw7NRGcxZqHO1YTtxxrEX0ok6rc/TCdbFyUfsn6gipxP6F9DUW5XCduK+7/RMHyI7pR+Ck4+EziIb3UtfFu2cTqLOyiTN5gjASRUcYzY4MYATGzixgRObn85fNpJjpuHSTUq6W65ObopPygjbCdvzbHBiACc2cGIDJzai+kyO3GZVp8nrvGT5cd8xddj14jhOei95zZzookH2WdUO4mqmhe+I497uQd4Ret2PwP8vD/Em2m2rSsyk9ruk27KSei+780vcupO7/3Vw8hcwGoZ6r+Q90e4EK7n3aXZXPYQ/p84PzvtkUT2EP2dT3S2vkCmODXOo7pZfPltXsvY95Erav/Hc+20nch0gaY4662nvzM4tGjnPqjt0F4xHKnOpYU4j62VvAAAAAAAAAAAAAAAAAAAAgB//AK+LUnlfZShzAAAAAElFTkSuQmCC"


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

    @Slot(str, int, float)
    def on_buy_stock(self, symbol, quantity, price):
        """Handle buy stock request from view
        
        Args:
            symbol: Stock symbol to buy
            quantity: Number of shares to buy
            price: Price per share
        """
        if not self.model.current_user_id:
            self.view.show_message("Please log in to trade", True)
            return

        if not symbol:
            self.view.show_message("Please select a stock first", True)
            return

        if quantity <= 0:
            self.view.show_message("Quantity must be greater than zero", True)
            return

        # Execute buy order through model
        success, result = self.model.execute_buy_order(symbol, quantity, price)

        if success:
            total_value = quantity * price
            self.view.show_message(f"Successfully bought {quantity} shares of {symbol} for ${total_value:.2f}")

            # Refresh holdings data
            self.model.get_user_holdings()
        else:
            error_msg = result.get("error", "Failed to execute buy order")
            self.view.show_message(error_msg, True)

    @Slot(str, int, float)
    def on_sell_stock(self, symbol, quantity, price):
        """Handle sell stock request from view
        
        Args:
            symbol: Stock symbol to sell
            quantity: Number of shares to sell
            price: Price per share
        """
        if not self.model.current_user_id:
            self.view.show_message("Please log in to trade", True)
            return

        if not symbol:
            self.view.show_message("Please select a stock first", True)
            return

        if quantity <= 0:
            self.view.show_message("Quantity must be greater than zero", True)
            return

        # Execute sell order through model
        success, result = self.model.execute_sell_order(symbol, quantity, price)

        if success:
            total_value = quantity * price
            self.view.show_message(f"Successfully sold {quantity} shares of {symbol} for ${total_value:.2f}")

            # Refresh holdings data
            self.model.get_user_holdings()
        else:
            error_msg = result.get("error", "Failed to execute sell order")
            self.view.show_message(error_msg, True)

    def _format_stock_data(self, symbol, api_data):
        """Format API data for display in the view
        
        Args:
            symbol: Stock symbol
            api_data: Raw data from API
            
        Returns:
            dict: Formatted data for view consumption
        """
        try:
            aggregate_data = json.loads(api_data.get("aggregateData", "{}"))
            print(api_data)
            return {
                "name": api_data.get("name", "Unknown Company"),
                "symbol": symbol,
                "description": api_data.get("description", "No description available"),
                "volume": api_data.get("volume", 0),
                "chart_data": aggregate_data.get("results", {}),
                "img": api_data.get("logoBase64", DEFAULT_ICON)
            }
        except Exception as e:
            print(f"Error formatting stock data: {str(e)}")

            # Return fallback data if formatting fails
            return {
                "name": f"{symbol} Inc.",
                "symbol": symbol,
                "description": "No description available",
                "volume": 0,
                "chart_data": {}
            }
