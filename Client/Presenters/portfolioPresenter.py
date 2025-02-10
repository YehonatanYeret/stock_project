# File: presenters/portfolio_presenter.py
from PySide6.QtCore import QObject

class PortfolioPresenter(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # Connect UI actions to model updates
        self.view.add_stock_signal.connect(self.add_stock)
        self.view.remove_stock_signal.connect(self.remove_stock)
        self.view.refresh_signal.connect(self.refresh_prices)

        # Connect model updates to UI
        self.model.portfolio_updated.connect(self.view.update_portfolio)

    def add_stock(self, symbol, company, quantity, avg_price):
        """Handles stock addition from the UI."""
        self.model.add_stock(symbol, company, quantity, avg_price)

    def remove_stock(self, symbol):
        """Handles stock removal from the UI."""
        self.model.remove_stock(symbol)

    def refresh_prices(self):
        """Handles price update requests from the UI."""
        self.model.update_prices()
