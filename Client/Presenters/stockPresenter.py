class StockPresenter:
    def __init__(self, model, view):
        """
        Initializes the presenter with the model and view.

        :param model: The stock data model.
        :param view: The stock search page (view).
        """
        self.model = model
        self.view = view

    def fetch_stock_data(self, ticker, start_date, end_date):
        """Fetch stock data from the model and update the view."""
        success, data, message = self.model.get_stock_details(ticker, start_date, end_date)

        if success:
            self.view.update_chart(ticker, start_date, end_date, data)  # Update the chart
        else:
            self.view.display_error(message)  # Display error message
