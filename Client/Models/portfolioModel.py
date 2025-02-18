# File: models/portfolio_model.py
from PySide6.QtCore import QObject, Signal
from datetime import datetime, timedelta
import random


class PortfolioModel(QObject):
    portfolio_updated = Signal(dict)
    stock_selected = Signal(dict)

    def __init__(self):
        super().__init__()
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
            }, {
                'date': '2024-02-10',
                'symbol': 'GOOGL',
                'type': 'BUY',
                'quantity': 10,
                'price': 2800.00,
                'fees': 4.99
            }, {
                'date': '2024-02-10',
                'symbol': 'GOOGL',
                'type': 'BUY',
                'quantity': 10,
                'price': 2800.00,
                'fees': 4.99
            }
        ]

    def refresh_data(self):
        # Simulate data refresh with small random changes
        for holding in self.portfolio_data['holdings']:
            holding['current_price'] *= (1 + random.uniform(-0.01, 0.01))
            holding['daily_change'] = random.uniform(-3, 3)
            holding['profit_loss'] = (holding['current_price'] - holding['buy_price']) * holding['quantity']

        self.portfolio_updated.emit(self.portfolio_data)

    def get_stock_details(self, symbol):
        # Find and return detailed data for selected stock
        for holding in self.portfolio_data['holdings']:
            if holding['symbol'] == symbol:
                return holding
        return None
