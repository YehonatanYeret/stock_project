class PortfolioModel:
    def __init__(self):
        self._portfolio = None
        self._performance_data = []
        self._holdings = []
        self._transactions = []
        self._observers = []
    
    def register_observer(self, observer):
        """Add an observer to be notified of model changes"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self):
        """Notify all observers of a change in the model"""
        for observer in self._observers:
            observer.model_updated()
    
    def set_portfolio(self, portfolio):
        """Set the portfolio data"""
        self._portfolio = portfolio
        self.notify_observers()
    
    def set_performance_data(self, performance_data):
        """Set the portfolio performance data"""
        self._performance_data = performance_data
        self.notify_observers()
    
    def set_holdings(self, holdings):
        """Set the portfolio holdings"""
        self._holdings = holdings
        self.notify_observers()
    
    def set_transactions(self, transactions):
        """Set the portfolio transactions"""
        self._transactions = transactions
        self.notify_observers()
    
    @property
    def portfolio(self):
        return self._portfolio
    
    @property
    def performance_data(self):
        return self._performance_data
    
    @property
    def holdings(self):
        return self._holdings
    
    @property
    def transactions(self):
        return self._transactions