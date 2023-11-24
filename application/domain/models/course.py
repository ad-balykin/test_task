from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Exchanger(str, Enum):
    binance = "binance"


class Currency(str, Enum):
    USD = "USD"
    USDT = "USDT"
    RUB = "RUB"
    ETH = "ETH"


class Course(BaseModel):
    id: str
    exchanger: Exchanger
    from_currency: Currency
    to_currency: Currency
    value: float
    next_attempt_time: datetime
