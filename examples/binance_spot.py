import json
from decimal import Decimal

import ccxt.async_support
from ccxt import ArgumentsRequired, BadRequest
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import InvalidOrder

from ccxt_ext.ccxt_ext import CCXTExtension
from spot_api import SpotApi


class BinanceSpot(CCXTExtension, ccxt.async_support.binance, SpotApi):

    @staticmethod
    def safe_float(dictionary, key, default_value=None):
        return CCXTExtension.safe_decimal(dictionary, key, default_value=None)

    @staticmethod
    def safe_float_2(dictionary, key1, key2, default_value=None):
        return CCXTExtension.safe_decimal_2(dictionary, key1, key2, default_value=None)

    async def fetch_markets(self, params=None):
        return await super().fetch_markets(params=params or {})

    async def fetch_order_book(self, symbol, since=None, limit=None, fromId=None, direct=None, params=None):
        return await super().fetch_order_book(symbol, limit, params=params or {})

    async def create_order(self, symbol, type, side, amount, price, clientOrderId, params=None):
        params = params or {}
        if clientOrderId:
            params['clientOrderId'] = clientOrderId
        return await super().create_order(symbol, type, side, amount, price, params)

    async def fetch_order(self, id, symbol, clientOrderId=None, params=None):
        params = params or {}
        if clientOrderId:
            params['clientOrderId'] = clientOrderId
        return await super().fetch_order(id, symbol, params)

    async def cancel_order(self, id, symbol, clientOrderId=None, params=None):
        params = params or {}
        if clientOrderId:
            params['clientOrderId'] = clientOrderId
        response = await super().cancel_order(id, symbol, params)
        return {
            'info': response['info']
        }

    async def fetch_orders(self, symbol, since=None, limit=None, fromId=None, direct=None, params=None):
        params = params or {}
        if fromId:
            params['orderId'] = fromId
        return await super().fetch_orders(symbol, since=since, limit=limit, params=params)

    async def fetch_open_orders(self, symbol, since=None, limit=None, fromId=None, direct=None, params=None):
        return await super().fetch_open_orders(symbol, since=since, limit=limit, params=params or {})

    async def fetch_closed_orders(self, symbol, since=None, limit=None, fromId=None, direct=None, params=None):
        orders = await self.fetch_orders(symbol=symbol, since=since, limit=limit, fromId=fromId, direct=direct, params=params or {})
        return self.filter_by_array(orders, 'status', values={'closed', 'canceled'}, indexed=False)

    async def fetch_my_trades(self, symbol, since=None, limit=None, fromId=None, direct=None, params=None):
        params = params or {}
        if fromId:
            params['fromId'] = fromId
        return await super().fetch_my_trades(symbol=symbol, since=since, limit=limit, params=params or {})

    async def fetch_order_trades(self, id, symbol, since=None, limit=None, params=None):
        return await super().fetch_order_trades(id, symbol=symbol, params=params or {})

    async def fetch_balance(self, params=None):
        return await super().fetch_balance(params=params or {})

    async def fetch_trading_fees(self, params=None):
        response = await super().fetch_trading_fees(params=params or {})
        return list(response.values())
