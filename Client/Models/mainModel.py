
from PySide6.QtCore import QObject, Signal

class MainModel(QObject):
    stock_data_updated = Signal(dict)
    portfolio_updated = Signal(list)

    def __init__(self):
        super().__init__()
        self._portfolio = []
        self._stocks = {}

    def add_to_portfolio(self, stock_info):
        """Placeholder for adding stock to portfolio"""
        self._portfolio.append(stock_info)
        self.portfolio_updated.emit(self._portfolio)

    def search_stock(self, symbol):
        """Placeholder for stock search logic"""
        # Future integration point with ASP.NET backend
        mock_stock_data = {
            "symbol": symbol,
            "name": f"Company {symbol}",
            "price": 100.00,
            "change": 1.5
        }
        self.stock_data_updated.emit(mock_stock_data)
        return mock_stock_data

    def get_portfolio(self):
        return self._portfolio