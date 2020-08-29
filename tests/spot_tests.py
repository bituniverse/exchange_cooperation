import time
from unittest import IsolatedAsyncioTestCase
from ccxt.async_support import binance

from examples.binance_spot import BinanceSpot
from . import schemas


class TestSpotAPIs(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.api = BinanceSpot({
            # note: DO NOT commit this
            'apiKey': 'your-api-key',
            'secret': 'your-api-secret',
            # 'verbose': True,
        })
        self.current_time_string = f'{int(time.time())}'
        self.order_id = None

    async def asyncTearDown(self) -> None:
        await self.api.close()

    async def test_fetch_markets(self):
        result = await self.api.fetch_markets()
        self.assertTrue(len(result) > 0)
        schemas.MARKETS_SCHEMA.validate(result)

    async def test_fetch_order_book(self):
        result = await self.api.fetch_order_book('BTC/USDT')
        schemas.ORDER_BOOK_SCHEMA.validate(result)

    async def test_create_order(self):
        result = await self.api.create_order('BTC/USDT', 'limit', 'buy', '0.001', 10000, self.current_time_string, None)
        schemas.ORDER_SCHEMA.validate(result)

    async def test_fetch_orders(self):
        result = await self.api.fetch_orders('BTC/USDT', limit=10)
        print(result)
        schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_order(self):
        result = await self.api.fetch_order(None, 'BTC/USDT', clientOrderId=self.current_time_string)
        print(result)
        self.order_id = result.get('id')
        schemas.ORDER_SCHEMA.validate(result)

    async def test_cancel_order(self):
        result = await self.api.cancel_order(None, 'BTC/USDT', clientOrderId=self.current_time_string)
        schemas.INFO_ONLY.validate(result)

    async def test_fetch_open_orders(self):
        result = await self.api.fetch_open_orders('BTC/USDT', limit=10)
        print(result)
        schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_closed_orders(self):
        result = await self.api.fetch_closed_orders('BTC/USDT', limit=10)
        print(result)
        schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_my_trades(self):
        result = await self.api.fetch_my_trades('BTC/USDT', limit=10)
        print(result)
        schemas.TRADES_SCHEMA.validate(result)

    async def test_fetch_order_trades(self):
        result = await self.api.fetch_order_trades(self.order_id, 'BTC/USDT', limit=10)
        print(result)
        schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_balance(self):
        result = await self.api.fetch_balance()
        print(result)
        schemas.BALANCE_SCHEMA.validate(result)

    async def test_fetch_trading_fees(self):
        result = await self.api.fetch_trading_fees()
        print(result)
        schemas.FEE_RATES_SCHEMA.validate(result)

