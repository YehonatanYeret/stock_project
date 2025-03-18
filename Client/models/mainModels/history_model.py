from PySide6.QtCore import QDateTime

from services.api_service import ApiService


class HistoryModel:
    """Model for transaction data and operations."""

    def __init__(self, api_service=None):
        """
        Initialize the transaction model.

        Args:
            api_service: API service for data operations
            user_id: Current user's ID
        """
        self.api_service = api_service or ApiService()
        self.user_id = None
        self.transactions = []

    def load_transactions(self):
        """
        Fetch transactions from the API.

        Returns:
            tuple: (success, data) where success is a boolean and data is the transactions list or error
        """
        success, data = self.api_service.get_transactions(self.user_id)
        if success:
            self.transactions = data
        return success, data

    def get_filtered_transactions(self, from_date, to_date, type_filter, search_text):
        """
        Filter transactions based on criteria.

        Args:
            from_date: Start date string in ISO format
            to_date: End date string in ISO format
            type_filter: Transaction type filter ("All", "Buy", or "Sell")
            search_text: Text to search in symbol or name

        Returns:
            list: Filtered transactions
        """

        filtered = []
        search_text = search_text.lower()

        for tx in self.transactions:
            # Parse transaction date
            tx_date = QDateTime.fromString(tx["date"].split("T")[0], "yyyy-MM-dd").date()
            filter_from_date = QDateTime.fromString(from_date, "yyyy-MM-dd").date() if from_date else None
            filter_to_date = QDateTime.fromString(to_date, "yyyy-MM-dd").date()

            # Check date range
            if (tx_date < filter_from_date and filter_from_date) or tx_date > filter_to_date:
                continue

            # Check transaction type
            if type_filter != "All" and tx["type"].lower() != type_filter.lower():
                continue

            # Check search text
            if search_text and not (search_text in tx["symbol"].lower() or search_text in tx["name"].lower()):
                continue

            filtered.append(tx)

        print(filtered)
        return filtered

    def set_user(self, user_id):
        """Set the current user ID."""
        self.user_id = user_id
