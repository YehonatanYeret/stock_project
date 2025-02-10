import requests

API_URL = "http://localhost:5039/api/Transaction"

class StockModel:
    def get_stock_details(self, ticker, start_date, end_date):
        """
        Fetch stock details from the API.

        :return: Tuple (success: bool, data: dict, message: str)
        """
        if not ticker or not start_date or not end_date:
            return False, None, "Ticker, start date, and end date are required."

        # Use `params` to pass query parameters safely
        params = {
            "ticker": ticker,
            "startDate": start_date,
            "endDate": end_date
        }

        try:
            response = requests.get(f"{API_URL}/getDetails", params=params)
            print(response)
            # Handle API response
            if response.status_code == 200:
                data = response.json().get("results")
                return True, data, "Stock data retrieved successfully!"
            
            elif response.status_code == 400:
                error_msg = response.json().get("message", "Invalid request parameters.")
                return False, None, f"Error: {error_msg}"
            
            elif response.status_code == 500:
                return False, None, "Server error. Please try again later."
            
            else:
                return False, None, f"Unexpected error: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return False, None, "Unable to connect to the server."
        except requests.exceptions.Timeout:
            return False, None, "The request timed out."
        except requests.exceptions.RequestException as e:
            return False, None, f"An unexpected error occurred: {str(e)}"
