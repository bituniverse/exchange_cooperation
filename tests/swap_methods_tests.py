import logging
import os
from unittest import IsolatedAsyncioTestCase

from examples.binance_swap import BinanceSwap
from . import schemas
from .test_keys import TEST_API_KEYS, TEST_CLASS

logging.basicConfig(level=logging.DEBUG)


class TestSwapAPIs(IsolatedAsyncioTestCase):
    api: BinanceSwap

    async def asyncSetUp(self) -> None:
        self.test_exchange = os.getenv('EXCHANGE', 'binance')
        exchange_class = TEST_CLASS[self.test_exchange]
        self.api = exchange_class(TEST_API_KEYS[self.test_exchange])
        self.test_symbol = 'BTC/USDT'
        self.fixed_client_order_id = 'bu_test_client_order_id'

    async def asyncTearDown(self) -> None:
        await self.api.close()

    async def test_fetch_markets(self):
        result = await self.api.fetch_markets()
        self.assertGreater(len(result), 0)
        # print(simplejson.dumps(result[0], indent=2))
        schemas.MARKETS_SCHEMA.validate(result)
    
    async def test_fetch_order_book(self):
        result = await self.api.fetch_order_book(self.test_symbol)
        schemas.ORDER_BOOK_SCHEMA.validate(result)
    
    async def test_create_order(self):
        result = await self.api.create_order(self.test_symbol, 'limit', 'buy', '0.001', 9000, self.fixed_client_order_id)
        # print(result)
        schemas.ORDER_SCHEMA.validate(result)
    
    async def test_fetch_orders(self):
        result = await self.api.fetch_orders(self.test_symbol, limit=10)
        # print(result)
        schemas.ORDERS_SCHEMA.validate(result)
    
    async def test_fetch_order(self):
        result = await self.api.fetch_order(None, 'BTC/USDT', clientOrderId=self.fixed_client_order_id)
        # print(result)
        schemas.ORDER_SCHEMA.validate(result)
    
    async def test_cancel_order(self):
        result = await self.api.cancel_order(None, 'BTC/USDT', clientOrderId=self.fixed_client_order_id)
        schemas.INFO_ONLY.validate(result)
    
    async def test_fetch_open_orders(self, should_contain_current_order=False):
        result = await self.api.fetch_open_orders(self.test_symbol, limit=10)
        # print(result)
        schemas.ORDERS_SCHEMA.validate(result)
    
    async def test_fetch_closed_orders(self, should_contain_current_order=False):
        result = await self.api.fetch_closed_orders('BTC/USDT', limit=10)
        # print(result)
        schemas.ORDERS_SCHEMA.validate(result)
    
    async def test_fetch_my_trades(self):
        result = await self.api.fetch_my_trades('BTC/USDT', limit=10)
        # print(result)
        schemas.TRADES_SCHEMA.validate(result)
    
    async def test_fetch_balance(self):
        result = await self.api.fetch_balance()
        # print(result)
        schemas.BALANCE_SCHEMA.validate(result)
    
    async def test_fetch_trading_fee_rates(self):
        result = await self.api.fetch_trading_fee_rates('BTC/USDT')
        print(result)
        schemas.FEE_RATES_SCHEMA.validate(result)
    
    async def test_fetch_positions(self):
        result = await self.api.fetch_positions('BTC/USDT')
        # print(result)
        schemas.POSITIONS_SCHEMA.validate(result)

    async def test_change_leverage(self):
        result = await self.api.change_leverage('BTC/USDT', None, 20)
        # print(result)
        schemas.INFO_ONLY.validate(result)
    
    async def test_change_margin_type(self):
        result = await self.api.change_margin_type('BTC/USDT', None, 'isolated')
        schemas.INFO_ONLY.validate(result)
    
    async def test_fetch_position_side(self):
        result = await self.api.fetch_position_side('BTC/USDT')
        # print(result)
        schemas.POSITION_SIDE_SCHEMA.validate(result)
    
    async def test_change_position_side(self):
        result = await self.api.change_position_side('BTC/USDT', 'single')
        # print(result)
        schemas.INFO_ONLY.validate(result)
    
    async def test_fetch_funding_records(self):
        result = await self.api.fetch_funding_records('BTC/USDT', limit=2)
        # print(result)
        schemas.FUNDING_FEEs_SCHEMA.validate(result)
    
    async def test_change_isolated_margin(self):
        result = await self.api.change_isolated_margin('BTC/USDT', 'both', 'asc', '0.1')
        # print(result)
        schemas.INFO_ONLY.validate(result)
