import time
from unittest import IsolatedAsyncioTestCase

from schema import Schema, Or

from examples.binance_swap import BinanceSwap
from . import swap_schemas


class TestSwapAPIs(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.api = BinanceSwap({
            # note: DO NOT commit this
            'apiKey': 'your-api-key',
            'secret': 'your-api-secret',
            # 'verbose': True,
        })
        self.current_time_string = f'{int(time.time())}'

    async def asyncTearDown(self) -> None:
        await self.api.close()

    async def test_fetch_markets(self):
        result = await self.api.fetch_markets()
        self.assertTrue(len(result) > 0)
        swap_schemas.MARKETS_SCHEMA.validate(result)

    async def test_fetch_order_book(self):
        result = await self.api.fetch_order_book('BTC/USDT')
        swap_schemas.ORDER_BOOK_SCHEMA.validate(result)

    async def test_create_order(self):
        result = await self.api.create_order('BTC/USDT', 'limit', 'buy', '0.001', 9000, self.current_time_string, None)
        swap_schemas.ORDER_SCHEMA.validate(result)

    async def test_fetch_orders(self):
        result = await self.api.fetch_orders('BTC/USDT', limit=10)
        # print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_order(self):
        result = await self.api.fetch_order(None, 'BTC/USDT', client_order_id=self.current_time_string)
        # print(result)
        swap_schemas.ORDER_SCHEMA.validate(result)

    async def test_cancel_order(self):
        result = await self.api.cancel_order(None, 'BTC/USDT', client_order_id=self.current_time_string)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_open_orders(self):
        result = await self.api.fetch_open_orders('BTC/USDT', limit=10)
        # print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_closed_orders(self):
        result = await self.api.fetch_closed_orders('BTC/USDT', limit=10)
        # print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_my_trades(self):
        result = await self.api.fetch_my_trades('BTC/USDT', limit=10)
        # print(result)
        swap_schemas.TRADES_SCHEMA.validate(result)

    async def test_fetch_balance(self):
        result = await self.api.fetch_balance()
        # print(result)
        swap_schemas.BALANCE_SCHEMA.validate(result)

    async def test_fetch_trading_fee_rates(self):
        result = await self.api.fetch_trading_fee_rates('BTC/USDT')
        # print(result)
        swap_schemas.FEE_RATES_SCHEMA.validate(result)

    async def test_fetch_positions(self):
        result = await self.api.fetch_positions('BTC/USDT')
        # print(result)
        swap_schemas.POSITIONS_SCHEMA.validate(result)

    async def test_change_leverage(self):
        result = await self.api.change_leverage('BTC/USDT', None, 20)
        # print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_change_margin_type(self):
        result = await self.api.change_margin_type('BTC/USDT', None, 'isolated')
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_position_side(self):
        result = await self.api.fetch_position_side('BTC/USDT')
        # print(result)
        swap_schemas.POSITION_SIDE_SCHEMA.validate(result)

    async def test_change_position_side(self):
        result = await self.api.change_position_side('BTC/USDT', 'single')
        # print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_funding_records(self):
        result = await self.api.fetch_funding_records('BTC/USDT', limit=2)
        # print(result)
        swap_schemas.FUNDING_FEEs_SCHEMA.validate(result)

    async def test_change_isolated_margin(self):
        result = await self.api.change_isolated_margin('BTC/USDT', 'both', 'asc', '0.1')
        # print(result)
        swap_schemas.INFO_ONLY.validate(result)

