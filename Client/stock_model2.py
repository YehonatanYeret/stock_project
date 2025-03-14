import requests

API_BASE_URL = "http://localhost:5039/api"


class StockModel:
    """
    Model responsible for handling API requests to fetch stock data.
    """

    def __init__(self):
        self.session = requests.Session()

    def get_portfolio(self, user_id):
        """Fetches portfolio data for a given user."""
        url = f"{API_BASE_URL}/trading/query/holdings/{user_id}"
        return self._send_request("GET", url)

    def get_stock_details(self, ticker, start_date, end_date):
        """Fetches details of a specific stock."""

        url = f"{API_BASE_URL}/transaction/query/getDetails?ticker={ticker}&startDate={start_date}&endDate={end_date}"
        return self._send_request("GET", url)

    def get_trade_history(self, user_id):
        """Fetches trade history for a given user."""
        url = f"{API_BASE_URL}/trading/query/trades/{user_id}"
        return self._send_request("GET", url)

    def _send_request(self, method, url):
        """Handles API requests and error logging."""
        try:
            response = self.session.request(method, url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return None


# Example usage
if __name__ == "__main__":
    model = StockModel()
    user_id = 1  # Replace with actual user ID
    print(model.get_portfolio(user_id))
    print(model.get_stock_details("AAPL", "2024-01-01", "2024-02-02"))
    print(model.get_trade_history(user_id))
