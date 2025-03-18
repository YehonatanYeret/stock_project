import datetime
from services.api_service import ApiService

class Holding:
    def __init__(self, Id, Symbol, Quantity, CurrentPrice, total_gain, total_gain_percentage):
        self.Id = Id
        self.Symbol = Symbol
        self.Quantity = Quantity
        self.CurrentPrice = CurrentPrice
        self.TotalValue = self.Quantity * self.CurrentPrice
        self.TotalGain = total_gain
        self.TotalGainPercentage = total_gain_percentage


class DashboardModel:
    def __init__(self):
        self.api_service = ApiService()
        self.holdings = []
        self.transactions = []
        self.user_id = None  # Store user ID for easy reference

    def fetch_holdings(self, user_id):
        """Fetch holdings from backend"""
        self.user_id = user_id  # Store user_id for future calls
        print(f"Fetching holdings for user {user_id} from backend")
        status, response = self.api_service.get_holdings(user_id)
        if status and isinstance(response, list):  # Assuming response is a list of holdings
            self.holdings = [
                Holding(h["id"], h["symbol"], h["quantity"], h["currentPrice"], h["totalGain"], h["totalGainPercentage"])
                for h in response
            ]
            print(self.holdings)
        else:
            print("Error fetching holdings:", response)

    def fetch_trades(self, user_id):
        """Fetch transactions from backend"""
        self.user_id = user_id
        print(f"Fetching trades for user {user_id} from backend")
        status, response = self.api_service.get_transactions(user_id)

        if status and isinstance(response, list):  # Assuming response is a list of trades
            self.transactions = [
                {"TradeDate": t["date"], "PortfolioValue": t.get("quantity", 0)*t.get("price", 0)*(-2*t.get("type", 0)+1)}
                for t in response
            ]
        else:
            print("Error fetching transactions:", response)

    def get_holdings(self):
        return self.holdings

    def get_transactions(self):
        return self.transactions

    def buy_stock(self, user_id, symbol, quantity):
        pass

    def sell_stock(self, holding_id, quantity):
        pass

    def get_cash_balance(self):
        return self.api_service.get_cash_balance(self.user_id)