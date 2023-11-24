from aiohttp import ClientSession

from .base import BaseExchangerAdapter
from application.domain.models.course import Currency


class BinanceAdapter(BaseExchangerAdapter):
    currency_map = {
        Currency.ETH: "ETH",
        Currency.USD: "USD",
        Currency.RUB: "RUB",
        Currency.USDT: "USDT",
    }

    async def fetch_rate(self, from_currency: Currency, to_currency: Currency) -> float:
        endpoint = f"{self._endpoint}/api/v3/ticker/price"

        from_mapped = self.currency_map[from_currency]
        to_mapped = self.currency_map[to_currency]
        params = {"symbol": f"{from_mapped}{to_mapped}"}

        async with ClientSession() as session:
            async with session.get(url=endpoint, params=params, ssl=False) as response:
                response.raise_for_status()
                response_body = await response.json()

        return float(response_body["price"])
