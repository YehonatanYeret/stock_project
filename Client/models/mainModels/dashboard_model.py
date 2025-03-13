import datetime

# ---------------------------------------------------------------------
# Holding Data Transfer Object
# ---------------------------------------------------------------------
class HoldingDto:
    def __init__(self, Id, Symbol, Quantity, CurrentPrice, TotalValue, TotalGain, TotalGainPercentage):
        self.Id = Id
        self.Symbol = Symbol
        self.Quantity = Quantity
        self.CurrentPrice = CurrentPrice
        self.TotalValue = TotalValue
        self.TotalGain = TotalGain
        self.TotalGainPercentage = TotalGainPercentage

# ---------------------------------------------------------------------
# Combined PortfolioModel with Observer Pattern + Mock Data
# ---------------------------------------------------------------------
class DashboardModel:
    """
    Holds portfolio data and logic for chart generation, money additions/removals, etc.
    Also implements the observer pattern to notify any registered observers when data changes.
    """

    def __init__(self):
        # Observer pattern fields
        self._observers = []

        # Example fields from your original observer-based code
        self._portfolio = None
        self._performance_data = []
        self._holdings = []
        self._transactions = []

        # Extra cash added/removed (for demonstration)
        self._cash = 0.0

        # Mock data for demonstration
        self._holdings = [
            HoldingDto(1, "AAPL", 10, 150.00, 1500.00, 200.00, 15.38),
            HoldingDto(2, "GOOGL", 5, 2800.00, 14000.00, -500.00, -3.45),
            HoldingDto(3, "TSLA", 8, 750.00, 6000.00, 800.00, 15.38),
            HoldingDto(4, "MSFT", 12, 320.00, 3840.00, 100.00, 2.67),
        ]

    # ---------------------------------------------------------------------
    # Observer Pattern Methods
    # ---------------------------------------------------------------------
    def register_observer(self, observer):
        """Add an observer to be notified of model changes."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self):
        """Notify all observers of a change in the model."""
        for observer in self._observers:
            observer.model_updated()

    # ---------------------------------------------------------------------
    # "Setters" that also notify observers
    # ---------------------------------------------------------------------
    def set_portfolio(self, portfolio):
        """Set the portfolio data (if you have an overall 'portfolio' object)."""
        self._portfolio = portfolio
        self.notify_observers()
    
    def set_performance_data(self, performance_data):
        """Set the portfolio performance data."""
        self._performance_data = performance_data
        self.notify_observers()
    
    def set_holdings(self, holdings):
        """Set the portfolio holdings (override the existing list)."""
        self._holdings = holdings
        self.notify_observers()
    
    def set_transactions(self, transactions):
        """Set the portfolio transactions."""
        self._transactions = transactions
        self.notify_observers()

    # ---------------------------------------------------------------------
    # "Getters" and logic for holdings, chart data, etc.
    # ---------------------------------------------------------------------
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

    def get_holdings(self):
        """Return the current list of holdings."""
        return self._holdings

    def get_total_value(self):
        """Sum of all holdings + extra cash."""
        portfolio_value = sum(h.TotalValue for h in self._holdings)
        return portfolio_value + self._cash

    def get_total_gain(self):
        """Sum of total gains for all holdings (not counting extra cash)."""
        return sum(h.TotalGain for h in self._holdings)

    def get_total_gain_pct(self):
        """
        Compute a simplistic gain percentage:
        (total_gain / total_value_of_holdings) * 100.
        """
        holdings_value = sum(h.TotalValue for h in self._holdings)
        if holdings_value == 0:
            return 0.0
        total_gain = sum(h.TotalGain for h in self._holdings)
        return (total_gain / holdings_value) * 100.0

    def add_money(self, amount):
        """Add extra cash to the portfolio."""
        self._cash += amount
        self.notify_observers()

    def remove_money(self, amount):
        """Remove cash from the portfolio (never going below 0)."""
        self._cash = max(0, self._cash - amount)
        self.notify_observers()

    def sell_stock(self, symbol):
        """Remove a holding from the list (simple example)."""
        self._holdings = [h for h in self._holdings if h.Symbol != symbol]
        self.notify_observers()

    def get_chart_data(self, months):
        """
        Generate sample chart data for 'months' months back from now.
        Returns a list of (datetime, value) for demonstration.
        """
        end_date = datetime.datetime.now()
        data = []
        base_value = 10000
        for i in range(months):
            month_date = end_date - datetime.timedelta(days=30 * (months - 1 - i))
            fluctuation = (i / 10) * base_value * (0.95 + 0.1 * (i % 3))
            value = base_value + fluctuation
            data.append((month_date, value))
        return data
