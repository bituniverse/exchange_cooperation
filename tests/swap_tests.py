import time
from unittest import IsolatedAsyncioTestCase



from exchanges.bitget_swap import  bitgetswap

from . import swap_schemas


class TestSwapAPIs(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.api = bitgetswap({
            # note: DO NOT commit this
            'apiKey': 'bg_b6bf2c1e88e352f6d03a0d02544f1354',
            'secret': '8ecba60d41f18be31a35371800a22628b5d9a8ec5f4b9a084d862f85770306f1',
            'password': '11111111'
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
        result = await self.api.fetch_order_book('BTC/USDT')
        print(result)
        swap_schemas.ORDER_BOOK_SCHEMA.validate(result)

    async def test_create_order(self):
        result = await self.api.create_order('BTC/USDT', 'market', 'buy', '100.23',None,None,"long")
        print(result)
        swap_schemas.ORDER_SCHEMA.validate(result)


    async def test_fetch_orders(self):
        result = await self.api.fetch_orders('BTC/USDT',limit=3)
        print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)


    async def test_fetch_order(self):
        result = await self.api.fetch_order("586058500090626013",'BTC/USDT',clientOrderId="586058500090626013")
        print(result)
        swap_schemas.ORDER_SCHEMA.validate(result)

    async def test_cancel_order(self):
        result = await self.api.cancel_order('692920682039738313', 'BTC/USDT',)
        print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_open_orders(self):
        result = await self.api.fetch_open_orders('BTC/USDT',limit=10)
        print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    async def test_fetch_closed_orders(self):
        result = await self.api.fetch_closed_orders('BTC/USDT', limit=10)
        print(result)
        swap_schemas.ORDERS_SCHEMA.validate(result)

    #Bitget platform is not support(swap)
    async def test_fetch_my_trades(self):
        result = await self.api.fetch_my_trades('BTC/USDT', limit=10)
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
        result = await self.api.change_leverage('BTC/USDT', 10, 'short')
        print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_change_margin_type(self):
        result = await self.api.change_margin_type('BTC/USDT', 'crossed',None)
        print(result)
        swap_schemas.INFO_ONLY.validate(result)

    async def test_fetch_position_side(self):
        result = await self.api.fetch_position_side('BTC/USDT')
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
        result = await self.api.fetch_funding_records("BTC/USDT",params={"pageIndex":1,"pageSize":1,"createDate":70})
        print(result)
        swap_schemas.FUNDING_FEEs_SCHEMA.validate(result)


    async def test_change_isolated_margin(self):
        result = await self.api.change_isolated_margin('BTC/USDT', 'long', 'asc', '0.1')
        print(result)
        swap_schemas.INFO_ONLY.validate(result)


