from PySide6.QtCore import QObject, Slot, QDateTime


class HistoryPresenter(QObject):
    """
    Presenter for transaction history.

    Connects the model and view, handling business logic.
    """

    def __init__(self, model, view, user_id=None):
        """
        Initialize the transaction history presenter.

        Args:
            model: TransactionModel instance
            view: TransactionHistoryView instance
        """
        super().__init__()
        self.model = model
        self.view = view

        if user_id:
            self.model.set_user(user_id)

        # Connect view signals to presenter slots
        self.view.filter_applied.connect(self.on_filter_applied)

        # Load initial data
        self.load_transactions()

    @Slot()
    def load_transactions(self):
        """Load transactions from the model and update the view."""
        success, data = self.model.load_transactions()

        if success:
            # Display all transactions initially
            self.apply_filters()
            print("Transactions loaded successfully", data)
        else:
            # Show error message
            self.view.show_error(data.get("error", "Failed to load transactions"))

    @Slot(str, str, str, str)
    def on_filter_applied(self, from_date, to_date, type_filter, search_text):
        """
        Handle filter application.

        Args:
            from_date: Start date string
            to_date: End date string
            type_filter: Transaction type filter
            search_text: Search text
        """
        self.apply_filters(from_date, to_date, type_filter, search_text)

    def apply_filters(self, from_date=None, to_date=None, type_filter="All", search_text=""):
        """
        Apply filters and update view.

        Args:
            from_date: Start date string (default: one month ago)
            to_date: End date string (default: today)
            type_filter: Transaction type filter (default: "All")
            search_text: Search text (default: "")
        """

        # Use default values if not provided
        if to_date is None:
            to_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")

        # Get filtered transactions from model
        filtered_transactions = self.model.get_filtered_transactions(
            from_date, to_date, type_filter, search_text
        )

        # Update view
        self.view.display_transactions(filtered_transactions)
