import datetime


class DashboardPresenter:
    def __init__(self, model, view, user_id=None):
        self.view = view
        self.model = model
        self.user_id = user_id

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
        cash_balance, total_gain, total_gain_pct = self.calculate_portfolio_summary(holdings)

        self.view.set_holdings_data(holdings)
        self.view.set_chart_data(self.get_chart_data(transactions))
        self.view.set_portfolio_summary(cash_balance, total_gain, total_gain_pct)

    def calculate_portfolio_summary(self, holdings):
        cash_balance = self.model.get_cash_balance()
        total_value = sum(h.TotalValue for h in holdings)
        total_gain = sum(h.TotalGain for h in holdings)#need to change
        return cash_balance, total_value, total_gain

    def get_chart_data(self, transactions):
        chart_data = []
        for trade in transactions:
            trade_date = datetime.datetime.fromisoformat(trade["TradeDate"])
            portfolio_value = trade["PortfolioValue"]
            chart_data.append((trade_date, portfolio_value))
        return chart_data

    def on_period_changed(self, period_text):
        print(f"Period changed to: {period_text}")  # Placeholder for filtering logic

    def on_buy_stock(self, symbol, quantity):
        if self.user_id is not None:
            self.model.buy_stock(self.user_id, symbol, quantity)
            self.model_updated()

    def on_sell_stock(self, symbol):
        holding = next((h for h in self.model.get_holdings() if h.Symbol == symbol), None)
        if holding:
            self.model.sell_stock(holding.Id, holding.Quantity)
            self.model_updated()

    def on_add_money(self):
        print("Add money clicked - Not implemented yet")

    def on_remove_money(self):
        print("Remove money clicked - Not implemented yet")
