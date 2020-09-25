import time
from unittest import IsolatedAsyncioTestCase



from exchanges.bitget_swap import  bitgetswap

from . import swap_schemas


class TestSwapAPIs(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.api = bitgetswap({
            # note: DO NOT commit this
            'apiKey': 'your-apikey',
            'secret': 'you-secret',
            'password': 'your-passphrase'
            # 'verbose': True,
        })
        self.current_time_string = f'{int(time.time())}'

    async def asyncTearDown(self) -> None:
        await self.api.close()


    async def test_fetch_markets(self):
        result = await self.api.fetch_markets()
        self.assertTrue(len(result) > 0)
        print(result)
        swap_schemas.MARKETS_SCHEMA.validate(result)


    async def test_fetch_order_book(self):
        result = await self.api.fetch_order_book('CMT_BTCUSDT')
        print(result)
        swap_schemas.ORDER_BOOK_SCHEMA.validate(result)

    # type 1 开多  2开空 3 平多 4 平空
    async def test_create_order(self):
        result = await self.api.create_order('CMT_BTCUSDT', 'market', 'buy', '100.23',None,params={"type":"1"})
        print(result)
        swap_schemas.ORDER_SCHEMA.validate(result)


    async def test_fetch_orders(self):
        result = await self.api.fetch_orders('CMT_BTCUSDT',limit=3)
        print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)


    async def test_fetch_order(self):
        result = await self.api.fetch_order(None,'CMT_BTCUSDT',clientOrderId="692920682039738313")
        print(result)
        swap_schemas.ORDER_SCHEMA.validate(result)

    async def test_cancel_order(self):
        result = await self.api.cancel_order(None, 'CMT_BTCUSDT',clientOrderId='692920682039738313')
        print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_open_orders(self):
        result = await self.api.fetch_open_orders('CMT_BTCUSDT',limit=10)
        print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_closed_orders(self):
        result = await self.api.fetch_closed_orders('CMT_BTCUSDT', limit=10)
        print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    #Bitget platform is not support(swap)
    async def test_fetch_my_trades(self):
        result = await self.api.fetch_my_trades('CMT_BTCUSDT', limit=10)
        # print(result)
        swap_schemas.TRADES_SCHEMA.validate(result)

    async def test_fetch_balance(self):
        result = await self.api.fetch_balance()
        print(result)
        swap_schemas.BALANCE_SCHEMA.validate(result)

    async def test_fetch_trading_fee_rates(self):
        result = await self.api.fetch_trading_fee_rates()
        print(result)
        swap_schemas.FEE_RATES_SCHEMA.validate(result)

    async def test_fetch_positions(self):
        result = await self.api.fetch_positions()
        print(result)
        swap_schemas.POSITIONS_SCHEMA.validate(result)

    async def test_change_leverage(self):
        result = await self.api.change_leverage('CMT_BTCUSDT', 10, 'short')
        print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_change_margin_type(self):
        result = await self.api.change_margin_type('CMT_BTCUSDT', 'crossed',None)
        print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_position_side(self):
        result = await self.api.fetch_position_side('CMT_BTCUSDT')
        print(result)
        swap_schemas.POSITION_SIDE_SCHEMA.validate(result)

    #Bitget platform is not support
    async def test_change_position_side(self):
        result = await self.api.change_position_side('BTC/USDT', 'single')
        # print(result)
        swap_schemas.INFO_ONLY.validate(result)

    #pageIndex  页码数
    #pageSize   每页的数量
    #createDate 从当天时间起可以查询的天数  最大90天
    async def test_fetch_funding_records(self):
        result = await self.api.fetch_funding_records("CMT_BTCUSDT",params={"pageIndex":1,"pageSize":1,"createDate":70})
        print(result)
        swap_schemas.FUNDING_FEEs_SCHEMA.validate(result)


    async def test_change_isolated_margin(self):
        result = await self.api.change_isolated_margin('CMT_BTCUSDT', 'long', 'asc', '0.1')
        print(result)
        swap_schemas.INFO_ONLY.validate(result)


