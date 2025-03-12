# File: models/portfolio_model.py
from PySide6.QtCore import QObject, Signal
from datetime import datetime, timedelta
import random
import requests
import json


class PortfolioModel(QObject):
    portfolio_updated = Signal(dict)
    stock_selected = Signal(dict)

    def __init__(self, use_api=False):
        super().__init__()
        self.use_api = use_api
        self.api_base_url = "http://localhost:5000/api"
        self._user_id = None
        self._generate_dummy_data()

    def _generate_dummy_data(self):
        # Generate dummy portfolio data
        self.portfolio_data = {
            'total_value': 100000.00,
            'daily_profit': 1250.50,
            'daily_profit_percentage': 1.25,
            'holdings': [
                {
                    'symbol': 'AAPL',
                    'quantity': 50,
                    'buy_price': 150.00,
                    'current_price': 175.25,
                    'daily_change': 2.5,
                    'profit_loss': 1262.50,
                    'market_cap': '2.85T',
                    'pe_ratio': 28.5
                },
                {
                    'symbol': 'GOOGL',
                    'quantity': 20,
                    'buy_price': 2800.00,
                    'current_price': 2950.75,
                    'daily_change': 1.8,
                    'profit_loss': 3015.00,
                    'market_cap': '1.95T',
                    'pe_ratio': 25.2
                }
            ],
            'performance_data': self._generate_performance_data(),
            'trade_history': self._generate_trade_history()
        }

    def _generate_performance_data(self):
        data = []
        base_value = 100000
        current_date = datetime.now()

        # Generate daily data for the past year
        for i in range(365):
            date = current_date - timedelta(days=i)
            change = random.uniform(-0.02, 0.02)
            base_value *= (1 + change)
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'value': round(base_value, 2)
            })
        return list(reversed(data))

    def _generate_trade_history(self):
        return [
            {
                'date': '2024-02-14',
                'symbol': 'AAPL',
                'type': 'BUY',
                'quantity': 25,
                'price': 150.00,
                'fees': 4.99
            },
            {
                'date': '2024-02-10',
                'symbol': 'GOOGL',
                'type': 'BUY',
                'quantity': 10,
                'price': 2800.00,
                'fees': 4.99
            },
            {
                'date': '2024-02-10',
                'symbol': 'GOOGL',
                'type': 'BUY',
                'quantity': 10,
                'price': 2800.00,
                'fees': 4.99
            },
            {
                'date': '2024-02-10',
                'symbol': 'GOOGL',
                'type': 'BUY',
                'quantity': 10,
                'price': 2800.00,
                'fees': 4.99
            }
        ]

    def _fetch_api_data(self, endpoint):
        """Fetch data from the API."""
        try:
            response = requests.get(f"{self.api_base_url}/{endpoint}")
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return None

    def refresh_data(self):
        """Refresh portfolio data from API or dummy data."""
        if self.use_api:
            try:
                # Call ASP.NET API endpoints
                portfolio_summary = self._fetch_api_data("portfolio/summary")
                holdings = self._fetch_api_data("portfolio/holdings")
                performance_data = self._fetch_api_data("portfolio/performance")
                trade_history = self._fetch_api_data("portfolio/trades")

                if all([portfolio_summary, holdings, performance_data, trade_history]):
                    # Update portfolio data with values from API
                    self.portfolio_data = {
                        'total_value': portfolio_summary['total_value'],
                        'daily_profit': portfolio_summary['daily_profit'],
                        'daily_profit_percentage': portfolio_summary['daily_profit_percentage'],
                        'holdings': holdings,
                        'performance_data': performance_data,
                        'trade_history': trade_history
                    }
                    self.portfolio_updated.emit(self.portfolio_data)
                else:
                    # Fall back to dummy data if any API call fails
                    self._fallback_to_dummy_refresh()
            except Exception as e:
                print(f"Error refreshing portfolio data: {e}")
                self._fallback_to_dummy_refresh()
        else:
            self._fallback_to_dummy_refresh()

    def _fallback_to_dummy_refresh(self):
        """Simulate data refresh with random changes."""
        for holding in self.portfolio_data['holdings']:
            holding['current_price'] *= (1 + random.uniform(-0.01, 0.01))
            holding['daily_change'] = random.uniform(-3, 3)
            holding['profit_loss'] = (holding['current_price'] - holding['buy_price']) * holding['quantity']

        # Update total value
        total_value = sum(holding['current_price'] * holding['quantity'] for holding in self.portfolio_data['holdings'])
        self.portfolio_data['total_value'] = total_value

        self.portfolio_updated.emit(self.portfolio_data)

    def get_stock_details(self, symbol):
        """Get detailed information for a selected stock."""
        if self.use_api:
            try:
                stock_details = self._fetch_api_data(f"stocks/{symbol}")
                if stock_details:
                    return stock_details
            except Exception as e:
                print(f"Error fetching stock details: {e}")

        # Fall back to dummy data
        for holding in self.portfolio_data['holdings']:
            if holding['symbol'] == symbol:
                return holding
        return None

    def get_performance_data(self, time_range="ALL"):
        """Get performance data for a specific time range."""
        if self.use_api:
            try:
                return self._fetch_api_data(f"portfolio/performance?range={time_range}")
            except Exception as e:
                print(f"Error fetching performance data: {e}")

        # Filter existing data based on range
        data = self.portfolio_data['performance_data']
        if time_range == "ALL":
            return data

        today = datetime.now()

        if time_range == "1D":
            days = 1
        elif time_range == "1W":
            days = 7
        elif time_range == "1M":
            days = 30
        elif time_range == "3M":
            days = 90
        elif time_range == "1Y":
            days = 365
        else:
            return data

        start_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
        return [point for point in data if point['date'] >= start_date]

    def set_user_id(self, user_id):
            self._user_id = user_id

    def get_user_id(self):
        return self._user_id
