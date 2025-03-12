from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Transaction:
    id: int
    stock_symbol: str
    type: TransactionType
    quantity: int
    price: Decimal
    total_amount: Decimal
    timestamp: datetime
