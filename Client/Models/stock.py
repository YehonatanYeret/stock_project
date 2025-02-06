from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Stock:
    symbol: str
    name: str
    current_price: Decimal
    quantity: int
    avg_purchase_price: Decimal
    total_value: Decimal
    profit_loss: Decimal
    profit_loss_percentage: Decimal
    last_updated: datetime