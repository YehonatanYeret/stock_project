# File: presenters/main_presenter.py
from PySide6.QtCore import QObject

class MainPresenter(QObject):
    def __init__(self, model, view):
        super().__init__()
        self._model = model
        self._view = view
        
        # Connect navigation buttons
        self._view.home_btn.clicked.connect(lambda: self._view.slide_to_page(0))
        self._view.portfolio_btn.clicked.connect(lambda: self._view.slide_to_page(1))
        self._view.search_btn.clicked.connect(lambda: self._view.slide_to_page(2))
        
    #     # Connect model signals
    #     self._model.stock_data_updated.connect(self.update_stock_data)
    #     self._model.portfolio_updated.connect(self.update_portfolio)

    # def update_stock_data(self, stock_data):
    #     """Update stock search page with retrieved data"""
    #     self._view.stock_search_page.update_stock_info(stock_data)

    # def update_portfolio(self, portfolio_data):
        """Update portfolio page with current portfolio"""
        self._view.portfolio_page.update_portfolio(portfolio_data)