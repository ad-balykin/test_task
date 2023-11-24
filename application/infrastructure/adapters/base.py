from abc import ABC, abstractmethod

from aiohttp import BaseConnector
from application.domain.models.course import Currency


class BaseExchangerAdapter(ABC):
    def __init__(self, endpoint: str, connector: BaseConnector):
        self._endpoint = endpoint
        self._connector = connector

    @abstractmethod
    async def fetch_rate(self, from_currency: Currency, to_currency: Currency) -> float:
        pass
