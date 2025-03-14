from PySide6.QtCore import QObject, Signal
from stock_model2 import StockModel

class StockPresenter(QObject):
    stock_data_received = Signal(dict)
    portfolio_data_received = Signal(list)
    order_processed = Signal(str)

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = StockModel()

        # חיבור אירועים מה-View לפונקציות ב-Presenter
        self.view.search_button.clicked.connect(self.fetch_stock_data)
        self.view.place_order_button.clicked.connect(self.process_order)

    def fetch_stock_data(self):
        """Fetch stock data from the model and update the view."""
        symbol = self.view.symbol_input.text().strip()
        start_date = self.view.start_date.date().toString("yyyy-MM-dd")
        end_date = self.view.end_date.date().toString("yyyy-MM-dd")

        if not symbol:
            self.view.stock_info.setText("⚠️ Please enter a stock symbol.")
            return

        stock_data = self.model.get_stock_details(symbol, start_date, end_date)

        if stock_data:
            self.stock_data_received.emit(stock_data)  # שולח נתונים ל-View
        else:
            self.view.stock_info.setText(f"❌ Could not fetch data for {symbol}")

    def process_order(self):
        """Process buy/sell order and update the UI."""
        order_type = "Buy" if self.view.buy_button.isChecked() else "Sell"
        quantity = self.view.quantity_input.value()

        # סימולציה של ביצוע עסקה (אין כרגע API להזמנות)
        response = f"✅ {order_type} order for {quantity} shares placed successfully!"
        self.order_processed.emit(response)  # שולח את התוצאה ל-View
