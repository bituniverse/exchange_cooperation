import asyncio
import logging
import os
import time
from decimal import Decimal
from functools import wraps
from unittest import IsolatedAsyncioTestCase

from examples.binance_swap import BinanceSwap
from . import schemas
from .test_keys import TEST_API_KEYS, TEST_CLASS

logging.basicConfig(level=logging.DEBUG)


def log_test(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logging.info(f'{func.__name__} started...')
        result = await func(*args, **kwargs)
        logging.info(f'{func.__name__} finished')
        return result
    return wrapper


class TestSwapAPIs(IsolatedAsyncioTestCase):
    api: BinanceSwap

    async def asyncSetUp(self) -> None:
        self.test_exchange = os.getenv('EXCHANGE', 'binance')
        exchange_class = TEST_CLASS[self.test_exchange]
        self.api = exchange_class(TEST_API_KEYS[self.test_exchange])
        self.test_symbol = 'BTC/USDT'
        self.test_side = 'buy'
        self.test_leverage = 20

        self.fixed_client_order_id = 'bu_test_client_order_id'

        self.current_order = None
        self.current_order_params = None
        self.current_position = None

    async def asyncTearDown(self) -> None:
        await self.test_clear_position()
        await self.api.close()

    @log_test
    async def test_fetch_markets(self):
        result = await self.api.fetch_markets()
        self.assertGreater(len(result), 0)
        # print(simplejson.dumps(result[0], indent=2))
        schemas.MARKETS_SCHEMA.validate(result)

    @log_test
    async def test_fetch_order_book(self):
        result = await self.api.fetch_order_book(self.test_symbol)
        schemas.ORDER_BOOK_SCHEMA.validate(result)

    async def get_buy_1_and_sell_1(self):
        order_book = await self.api.fetch_order_book(self.test_symbol)
        return order_book['bids'][0][0], order_book['asks'][0][0]

    @log_test
    async def test_fetch_open_orders(self, should_contain_current_order=False):
        result = await self.api.fetch_open_orders(self.test_symbol, limit=10)
        # print(result)
        schemas.ORDERS_SCHEMA.validate(result)
        if should_contain_current_order:
            current_order = result[-1]
            self.check_current_order(current_order)
        else:
            for order in result:
                self.assertNotEqual(order['id'], self.current_order['id'])

    @log_test
    async def test_fetch_closed_orders(self, should_contain_current_order=False):
        result = await self.api.fetch_closed_orders(self.test_symbol, limit=10)
        # print(result)
        schemas.ORDERS_SCHEMA.validate(result)
        if should_contain_current_order:
            current_order = result[-1]
            self.check_current_order(current_order)
        else:
            for order in result:
                self.assertNotEqual(order['id'], self.current_order['id'])

    @staticmethod
    def random_client_order_id():
        return f't{int(time.time())}'

    async def get_order_params(self, should_trade=False):
        await self.api.load_markets()
        market = self.api.market(self.test_symbol)
        bid1, ask1 = await self.get_buy_1_and_sell_1()

        if should_trade:
            price = Decimal(str(ask1)) * Decimal('1.1')
        else:
            price = Decimal(str(bid1)) / Decimal('1.5')

        price = self.api.price_to_precision(self.test_symbol, price)

        min_amount = market['limits']['amount']['min']
        min_cost = market['limits'].get('cost') and market['limits'].get('cost').get('min')
        if min_cost:
            min_amount = max(Decimal(min_cost) / price, min_amount) * 2
            min_amount = self.api.amount_to_precision(self.test_symbol, min_amount)

        params = {
            'symbol': self.test_symbol,
            'type': 'limit',
            'side': self.test_side,
            'amount': str(min_amount),
            'price': price,
        }

        if self.api.has.get('clientOrderIdSupport'):
            params['clientOrderId'] = self.random_client_order_id()

        self.current_order_params = params

        logging.info(f"create order params: {params}")
        return params

    def check_current_order(self, order):
        schemas.ORDER_SCHEMA.validate(order)
        for k, v in self.current_order_params.items():
            self.assertEqual(str(order.get(k)).rstrip('0.'), str(v).rstrip('0.'), f'field: {k}')

    @log_test
    async def test_create_untrade_order(self):
        order_params = await self.get_order_params()
        order = await self.api.create_order(**order_params)
        self.current_order = order
        self.check_current_order(order)

    @log_test
    async def test_create_trade_order(self):
        order_params = await self.get_order_params(should_trade=True)
        order = await self.api.create_order(**order_params)
        self.current_order = order
        self.check_current_order(order)

    @log_test
    async def test_fetch_current_order(self, update_current_order=False):
        self.assertIsNotNone(self.current_order)
        order = await self.api.fetch_order(self.current_order['id'], self.test_symbol)
        self.check_current_order(order)
        if update_current_order:
            self.current_order = order

    @log_test
    async def test_cancel_current_order(self):
        self.assertIsNotNone(self.current_order)
        result = await self.api.cancel_order(self.current_order['id'], self.test_symbol)
        schemas.INFO_ONLY.validate(result)

    @log_test
    async def test_fetch_current_position(self, check_position_diff_with_current_order=False):
        result = await self.api.fetch_positions(self.test_symbol)
        # print(result)
        schemas.POSITIONS_SCHEMA.validate(result)
        if check_position_diff_with_current_order:
            self.assertIsNotNone(self.current_order)
            sign = 1 if self.current_order['side'] == 'buy' else -1
            origin_position = self.current_position and self.current_position['position'] or 0
            order_traded = self.current_order['filled']
            expect_position = Decimal(origin_position) + sign * Decimal(order_traded)
            real_position = len(result) > 0 and Decimal(str(result[0]['position'])) or 0
            self.assertEqual(expect_position, real_position)
        else:
            if result:
                self.current_position = result[0]

    @log_test
    async def test_common_order_operations(self):
        await self.test_create_untrade_order()
        await asyncio.sleep(1)
        await self.test_fetch_current_order()
        await self.test_fetch_open_orders(should_contain_current_order=True)
        await self.test_fetch_closed_orders(should_contain_current_order=False)
        await self.test_cancel_current_order()
        await asyncio.sleep(1)
        await self.test_fetch_open_orders(should_contain_current_order=False)
        await self.test_fetch_closed_orders(should_contain_current_order=True)

    @log_test
    async def test_position(self):
        await self.test_fetch_current_position()
        await self.test_create_trade_order()
        await asyncio.sleep(1)
        await self.test_fetch_current_order(update_current_order=True)
        await self.test_fetch_closed_orders(should_contain_current_order=True)
        await self.test_fetch_current_position(check_position_diff_with_current_order=True)

    @log_test
    async def test_leverage(self):
        await self.test_clear_position()

        # set leverage twice to test duplicated case. The implement should NOT raise any error
        await self.api.change_leverage(self.test_symbol, self.test_leverage)
        await self.api.change_leverage(self.test_symbol, self.test_leverage)

        await self.test_create_trade_order()
        await asyncio.sleep(1)
        await self.test_fetch_current_position()
        self.assertEqual(int(self.current_position['leverage']), self.test_leverage)

    @log_test
    async def test_clear_position(self):
        await self.test_fetch_current_position()
        if self.current_position:
            position = Decimal(self.current_position['position'])
            if not position:
                return
            position_side = self.current_position.get('positionSide')
            if not position_side or (position_side and position_side == 'both'):
                side = 'sell' if position > 0 else 'buy'
            else:
                side = 'sell' if position_side == 'long' else 'buy'
            await self.api.create_order(self.test_symbol, 'market', side, str(position.normalize()))

