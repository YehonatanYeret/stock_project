# File: presenters/portfolio_presenter.py
from PySide6.QtCore import QObject, Qt
from PySide6.QtCharts import QLineSeries, QDateTimeAxis, QValueAxis
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
        self._view.chart_range_changed.connect(self._update_chart_range)

        # Connect model signals
        self._model.portfolio_updated.connect(self.update_portfolio_view)

        # Setup initial state
        self.current_table_view = 'holdings'
        self.setup_chart()
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

        # Access the chart from the view
        chart_view = self._view.chart_view
        chart = chart_view.chart()

        # Remove existing series and axes to prevent duplication
        chart.removeAllSeries()
        for axis in chart.axes(Qt.Vertical):
            chart.removeAxis(axis)
        for axis in chart.axes(Qt.Horizontal):
            chart.removeAxis(axis)

        # Add the new series
        chart.addSeries(series)

        # Create new axes with the chart as parent
        axis_x = QDateTimeAxis(chart)
        axis_x.setFormat("MMM dd")
        axis_x.setTitleText("Date")

        axis_y = QValueAxis(chart)
        axis_y.setLabelFormat("$%.2f")
        axis_y.setTitleText("Portfolio Value")

        # Add axes to the chart using explicit enum values
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        # Attach series to the newly added axes
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def update_holdings_table(self, holdings):
        """
        Update the table with holdings data.

        Args:
            holdings: List of dictionaries containing holdings information
        """
        # Clear the table first - this fixes the duplication bug

        self._view.table.clearContents()
        self._view.table.setRowCount(0)
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
            else:
                profit_loss_text = f"+{profit_loss_text}"
            self._view.table.setItem(row, 5, QTableWidgetItem(profit_loss_text))

    def update_trade_history(self, history):
        """
        Update the table with trade history data.

        Args:
            history: List of dictionaries containing trade history information
        """
        # Clear the table first - this fixes the duplication bug
        self._view.table.setRowCount(0)
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
            # Emit signal to notify about stock selection
            self._model.stock_selected.emit(stock_data)

    def _toggle_table_view(self):
        """Toggle between holdings and trade history table views."""
        if self.current_table_view == 'holdings':
            self.current_table_view = 'trade_history'
            self._view.view_toggle.setText("Switch to Holdings")
        else:
            self.current_table_view = 'holdings'
            self._view.view_toggle.setText("Switch to Trade History")

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

    def setup_chart(self):
        """Setup the chart with zooming and panning."""
        # Set default time range
        if self._view.time_range_buttons:
            self._view.time_range_buttons[-1].setChecked(True)  # Select "ALL" by default

    def _update_chart_range(self, range_text):
        """
        Update chart data based on selected time range.

        Args:
            range_text: String indicating the selected time range
        """
        # Get filtered performance data for the selected range
        filtered_data = self._model.get_performance_data(range_text)

        # Update the chart
        if filtered_data:
            self.update_chart_data(filtered_data)

    def get_user_id(self):
        """Return the user ID from the model."""
        return self._model.get_user_id()