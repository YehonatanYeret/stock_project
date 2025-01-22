from dataclasses import dataclass
from decimal import Decimal
from typing import List
from .stock import Stock

@dataclass
class Portfolio:
    stocks: List[Stock]
    total_value: Decimal
    total_profit_loss: Decimal
    total_profit_loss_percentage: Decimal
    last_updated: datetime