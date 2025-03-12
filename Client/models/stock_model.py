class StockModel:
    def __init__(self):
        self._stocks = []
        self._current_stock = None
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
    
    def set_stocks(self, stocks):
        """Set the list of stocks"""
        self._stocks = stocks
        self.notify_observers()
    
    def set_current_stock(self, stock):
        """Set the currently selected stock"""
        self._current_stock = stock
        self.notify_observers()
    
    def get_stocks(self):
        """Get all stocks"""
        return self._stocks
    
    def get_stock(self, stock_id):
        """Get a specific stock by ID"""
        for stock in self._stocks:
            if stock['id'] == stock_id:
                return stock
        return None
    
    @property
    def current_stock(self):
        return self._current_stock