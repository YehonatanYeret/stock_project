# File: models/portfolio_model.py
import json
from PySide6.QtCore import QObject, Signal
import random  # Mocking stock prices

class PortfolioModel(QObject):
    stock_data_updated = Signal(dict)
    portfolio_updated = Signal(list)

    def __init__(self):
        super().__init__()
        self.stocks = []
        self.load_portfolio()

    def add_stock(self, symbol, company, quantity, avg_price):
        """Adds a new stock to the portfolio."""
        stock = {
            "symbol": symbol.upper(),
            "company": company,
            "quantity": quantity,
            "avg_price": avg_price,
            "current_price": self.get_stock_price(symbol),
        }
        stock["market_value"] = stock["quantity"] * stock["current_price"]
        stock["profit_loss"] = stock["market_value"] - (stock["quantity"] * stock["avg_price"])
        self.stocks.append(stock)
        self.portfolio_updated.emit(self.stocks)
        self.save_portfolio()

    def remove_stock(self, symbol):
        """Removes a stock from the portfolio."""
        self.stocks = [s for s in self.stocks if s["symbol"] != symbol.upper()]
        self.portfolio_updated.emit(self.stocks)
        self.save_portfolio()

    def update_prices(self):
        """Fetches (or mocks) live stock prices and updates portfolio."""
        for stock in self.stocks:
            stock["current_price"] = self.get_stock_price(stock["symbol"])
            stock["market_value"] = stock["quantity"] * stock["current_price"]
            stock["profit_loss"] = stock["market_value"] - (stock["quantity"] * stock["avg_price"])

        self.portfolio_updated.emit(self.stocks)
        self.save_portfolio()

    def get_stock_price(self, symbol):
        """Mock function to simulate getting stock prices."""
        return round(random.uniform(50, 300), 2)  # Random price for demo

    def save_portfolio(self):
        """Saves portfolio data to a JSON file."""
        with open("portfolio.json", "w") as file:
            json.dump(self.stocks, file, indent=4)

    def load_portfolio(self):
        """Loads portfolio data from a JSON file."""
        try:
            with open("portfolio.json", "r") as file:
                self.stocks = json.load(file)
                self.portfolio_updated.emit(self.stocks)
        except (FileNotFoundError, json.JSONDecodeError):
            self.stocks = []
