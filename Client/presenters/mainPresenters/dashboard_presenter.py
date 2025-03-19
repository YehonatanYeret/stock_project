import datetime
from PySide6.QtCore import Signal, QObject

class DashboardPresenter(QObject):
    move_to_sell_signal = Signal(str)
    def __init__(self, model, view, user_id=None):
        super().__init__()
        self.view = view
        self.model = model
        self.user_id = user_id

        self.view.add_money_clicked.connect(self.on_add_money)
        self.view.remove_money_clicked.connect(self.on_remove_money)
        self.view.on_period_changed.connect(self.on_period_changed)
        self.view.on_sell_clicked.connect(self.move_to_sell_signal)

        # If a valid user_id is provided at initialization, fetch initial data.
        if self.user_id is not None:
            self.model.fetch_holdings(self.user_id)
            self.model.fetch_trades(self.user_id)
            self.model_updated()

    def model_updated(self):
        """Update the View with new data from the Model"""
        if self.user_id is None:
            return

        holdings = self.model.get_holdings()
        transactions = self.model.get_transactions()
        cash_balance, total_value, total_gain = self.calculate_portfolio_summary(holdings)

        self.view.set_holdings_data(holdings)
        self.view.set_chart_data(self.get_chart_data(transactions))
        self.view.set_cash_balance(cash_balance)
        self.view.set_total_value(total_value)
        self.view.set_total_gain(total_gain)

    def calculate_portfolio_summary(self, holdings):
        cash_balance = self.model.get_cash_balance()
        total_value = sum(h.TotalValue for h in holdings)
        total_gain = self.model.get_total_gain()
        return cash_balance, total_value, total_gain

    def get_chart_data(self, transactions):
        """Converts raw transaction data into chart-friendly format."""
        chart_data = []
        for trade in transactions:
            trade_date = datetime.datetime.fromisoformat(trade["TradeDate"])
            portfolio_value = trade["PortfolioValue"]
            chart_data.append((trade_date, portfolio_value))
        return chart_data

    def on_period_changed(self, period_text):
        """Handles period change and filters transactions accordingly."""
        print(f"Period changed to: {period_text}")

        # Map period to days
        period_map = {
            "Last 3 Months": 90,
            "Last 6 Months": 180,
            "Last Year": 365
        }
        days = period_map.get(period_text)  # Returns None for "All Time"

        # Fetch transactions and transform them into chart data
        transactions = self.model.get_transactions()
        chart_data = self.get_chart_data(transactions)

        if days is not None:
            # Filter transactions within the selected time range
            now = datetime.datetime.now()
            filtered_transactions = [(date, value) for date, value in chart_data if (now - date).days <= days]
            print(filtered_transactions)
            self.view.set_chart_data(filtered_transactions)
        else:
            # Show all data for "All Time"
            self.view.set_chart_data(chart_data)

    def on_add_money(self):
        new_cash_balance = self.model.add_money(self.user_id, 500.0)
        if new_cash_balance is not None:
            self.view.set_cash_balance(new_cash_balance)

    def on_remove_money(self):
        new_cash_balance = self.model.remove_money(self.user_id, 500.0)
        if new_cash_balance is not None:
            self.view.set_cash_balance(new_cash_balance)
