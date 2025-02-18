from PySide6.QtCore import QObject, Qt
from PySide6.QtCharts import QLineSeries, QDateTimeAxis, QValueAxis, QChart
from PySide6.QtWidgets import QTableWidgetItem
from datetime import datetime, timedelta

class PortfolioPresenter(QObject):
    """
    Presenter class that handles the business logic between PortfolioModel and PortfolioPage.
    Processes data and updates the view according to user interactions.
    """

    def __init__(self, model, view):
        """
        Initialize the presenter with model and view references.
        
        Args:
            model: PortfolioModel instance
            view: PortfolioPage instance
        """
        super().__init__()
        self._model = model
        self._view = view

        # Connect view signals
        self._view.refresh_requested.connect(self._model.refresh_data)
        self._view.table.itemClicked.connect(self._handle_table_click)
        self._view.view_toggle.clicked.connect(self._toggle_table_view)

        # Connect model signals
        self._model.portfolio_updated.connect(self.update_portfolio_view)

        # Setup initial state
        self.current_table_view = 'holdings'
        self.setup_enhanced_chart()
        self.setup_table_view('holdings')

        # Initial data update
        self.update_portfolio_view(self._model.portfolio_data)

    def update_portfolio_view(self, data):
        """
        Update all view components with new portfolio data.
        
        Args:
            data: Dictionary containing portfolio data from the model
        """
        # Update portfolio value and daily change
        self._view.update_portfolio_value(
            data['total_value'],
            data['daily_profit'],
            data['daily_profit_percentage']
        )

        # Update chart
        self.update_chart_data(data['performance_data'])

        # Update table based on current view
        if self.current_table_view == 'holdings':
            self.update_holdings_table(data['holdings'])
        else:
            self.update_trade_history(data['trade_history'])

    def update_chart_data(self, performance_data):
        """
        Update the performance chart with new data.
        
        Args:
            performance_data: List of dictionaries containing date and value pairs
        """
        series = QLineSeries()

        for point in performance_data:
            date = datetime.strptime(point['date'], '%Y-%m-%d')
            timestamp = int(date.timestamp() * 1000)
            series.append(timestamp, point['value'])

        self._view.update_chart_data(series)

    def update_holdings_table(self, holdings):
        """
        Update the table with holdings data.
        
        Args:
            holdings: List of dictionaries containing holdings information
        """
        self._view.table.setRowCount(len(holdings))

        for row, holding in enumerate(holdings):
            # Symbol
            self._view.table.setItem(row, 0, QTableWidgetItem(holding['symbol']))
            # Quantity
            self._view.table.setItem(row, 1, QTableWidgetItem(str(holding['quantity'])))
            # Buy Price
            self._view.table.setItem(row, 2, QTableWidgetItem(f"${holding['buy_price']:,.2f}"))
            # Current Price
            self._view.table.setItem(row, 3, QTableWidgetItem(f"${holding['current_price']:,.2f}"))
            # Daily Change
            self._view.table.setItem(row, 4, QTableWidgetItem(f"{holding['daily_change']:,.2f}%"))
            # Profit/Loss
            profit_loss = holding['profit_loss']
            profit_loss_text = f"${abs(profit_loss):,.2f}"
            if profit_loss < 0:
                profit_loss_text = f"-{profit_loss_text}"
            self._view.table.setItem(row, 5, QTableWidgetItem(profit_loss_text))

    def update_trade_history(self, history):
        """
        Update the table with trade history data.
        
        Args:
            history: List of dictionaries containing trade history information
        """
        self._view.table.setRowCount(len(history))

        for row, trade in enumerate(history):
            self._view.table.setItem(row, 0, QTableWidgetItem(trade['date']))
            self._view.table.setItem(row, 1, QTableWidgetItem(trade['symbol']))
            self._view.table.setItem(row, 2, QTableWidgetItem(trade['type']))
            self._view.table.setItem(row, 3, QTableWidgetItem(str(trade['quantity'])))
            self._view.table.setItem(row, 4, QTableWidgetItem(f"${trade['price']:,.2f}"))
            self._view.table.setItem(row, 5, QTableWidgetItem(f"${trade['fees']:,.2f}"))

    def _handle_table_click(self, item):
        """
        Handle clicks on table items.
        
        Args:
            item: QTableWidgetItem that was clicked
        """
        if self.current_table_view == 'holdings':
            row = item.row()
            symbol = self._view.table.item(row, 0).text()
            self._show_stock_details(symbol)

    def _show_stock_details(self, symbol):
        """
        Show detailed information for a selected stock.
        
        Args:
            symbol: Stock symbol to show details for
        """
        stock_data = self._model.get_stock_details(symbol)
        if stock_data:
            # Update the view with stock details (implement in view if needed)
            pass

    def _toggle_table_view(self):
        """Toggle between holdings and trade history table views."""
        self.current_table_view = 'trade_history' if self.current_table_view == 'holdings' else 'holdings'
        self.setup_table_view(self.current_table_view)

    def setup_table_view(self, view_type):
        """
        Configure table columns and data based on view type.
        
        Args:
            view_type: String indicating the type of view ('holdings' or 'trade_history')
        """
        if view_type == 'holdings':
            self._view.set_holdings_view()
            self.update_holdings_table(self._model.portfolio_data['holdings'])
        else:
            self._view.set_trade_history_view()
            self.update_trade_history(self._model.portfolio_data['trade_history'])

    def setup_enhanced_chart(self):
        """Setup the enhanced chart with zooming and panning."""
        chart = self._view.chart_view.chart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)
        chart.legend().hide()

        # Connect time range buttons
        for btn in self._view.time_range_buttons:
            btn.clicked.connect(lambda checked, b=btn: self._update_chart_range(b.text()))

    def _update_chart_range(self, range_text):
        """
        Update chart data based on selected time range.
        
        Args:
            range_text: String indicating the selected time range
        """
        # Implementation would filter performance data based on the selected range
        # For now, just update with all data
        self.update_chart_data(self._model.portfolio_data['performance_data'])