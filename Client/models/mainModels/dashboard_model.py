import datetime

from PySide6.QtCore import Signal
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
        status, response = self.api_service.get_holdings(user_id)
        if status and isinstance(response, list):  # Assuming response is a list of holdings
            self.holdings = [
                Holding(h["id"], h["symbol"], h["quantity"], h["currentPrice"], h["totalGain"],
                        h["totalGainPercentage"])
                for h in response
            ]
        else:
            print("Error fetching holdings:", response)

    def fetch_trades(self, user_id):
        """Fetch transactions from backend"""
        self.user_id = user_id
        status, response = self.api_service.get_transactions(user_id)

        if status and isinstance(response, list):  # Assuming response is a list of trades
            self.transactions = [
                {"TradeDate": t["date"],
                 "PortfolioValue": t.get("quantity", 0) * t.get("price", 0) * (2 * t.get("type", 0) - 1)}
                for t in response
            ]
            self.transactions.sort(key=lambda x: x["TradeDate"])
        else:
            print("Error fetching transactions:", response)

    def get_holdings(self):
        return self.holdings

    def get_transactions(self):
        return self.transactions

    def buy_stock(self, user_id, symbol, quantity):
        pass

    def sell_stock(self, holding_id, quantity):
        # Unpack the tuple into corresponding variables
        _, trade = self.api_service.sell_stock(holding_id, quantity)
        print("Trade response:", trade)
        self.holdings = [h for h in self.holdings if h.Id != holding_id]
        self.transactions.append({"TradeDate": trade["date"],
                                  "PortfolioValue": trade["quantity"] * trade["price"] * (2 * trade["type"] - 1)})

    def get_cash_balance(self):
        return self.api_service.get_cash_balance(self.user_id)

    def get_total_gain(self):
        return self.api_service.get_profit(self.user_id)

    def add_money(self, user_id, amount):
        return self.api_service.add_money(user_id, amount)

    def remove_money(self, user_id, amount):
        return self.api_service.remove_money(user_id, amount)
