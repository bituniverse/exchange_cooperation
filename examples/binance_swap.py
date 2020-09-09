import json
from decimal import Decimal

import ccxt.async_support
from ccxt import ArgumentsRequired, BadRequest

from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce

from ccxt_ext.ccxt_ext import CCXTExtension
from ccxt_ext.errors import ChangeMarginTypeError, ChangePositionError
from swap_api import SwapApi


class BinanceSwap(SwapApi, CCXTExtension, ccxt.async_support.binance):

    # ------------------------------------------------------------------------------------------------------------------

    def describe(self):
        return self.deep_extend(super().describe(), {
            'id': 'binance',
            'name': 'Binance',
            'countries': ['JP', 'MT'],  # Japan, Malta
            'rateLimit': 500,
            'certified': True,
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/29604020-d5483cdc-87ee-11e7-94c7-d1a8d9169293.jpg',
                'test': {
                    'fapiPublic': 'https://testnet.binancefuture.com/fapi/v1',
                    'fapiPrivate': 'https://testnet.binancefuture.com/fapi/v1',
                },
                'api': {
                    'web': 'https://www.binance.com',
                    'wapi': 'https://api.binance.com/wapi/v3',
                    'sapi': 'https://api.binance.com/sapi/v1',
                    'fapiPublic': 'https://fapi.binance.com/fapi/v1',
                    'fapiPrivate': 'https://fapi.binance.com/fapi/v1',
                    'fapiPrivatev2': 'https://fapi.binance.com/fapi/v2',
                    'public': 'https://api.binance.com/api/v3',
                    'private': 'https://api.binance.com/api/v3',
                    'v3': 'https://api.binance.com/api/v3',
                    'v1': 'https://api.binance.com/api/v1',
                },
                'www': 'https://www.binance.com',
                'referral': 'https://www.binance.com/?ref=10205187',
                'doc': [
                    'https://binance-docs.github.io/apidocs/spot/en',
                ],
                'api_management': 'https://www.binance.com/en/usercenter/settings/api-management',
                'fees': 'https://www.binance.com/en/fee/schedule',
            },
            'api': {
                'web': {
                    'get': [
                        'exchange/public/product',
                        'assetWithdraw/getAllAsset.html',
                    ],
                },
                # the API structure below will need 3-layer apidefs
                'fapiPublic': {
                    'get': [
                        'ping',
                        'time',
                        'exchangeInfo',
                        'depth',
                        'trades',
                        'historicalTrades',
                        'aggTrades',
                        'klines',
                        'fundingRate',
                        'premiumIndex',
                        'ticker/24hr',
                        'ticker/price',
                        'ticker/bookTicker',
                        'allForceOrders',
                        'openInterest',
                        'leverageBracket',
                    ],
                },
                'fapiPrivate': {
                    'get': [
                        'allOrders',
                        'openOrder',
                        'openOrders',
                        'order',
                        'account',
                        'balance',
                        'positionSide/dual',
                        'positionMargin/history',
                        'positionRisk',
                        'userTrades',
                        'income',
                    ],
                    'post': [
                        'batchOrders',
                        'positionSide/dual',
                        'positionMargin',
                        'marginType',
                        'order',
                        'leverage',
                        'listenKey',
                    ],
                    'put': [
                        'listenKey',
                    ],
                    'delete': [
                        'batchOrders',
                        'order',
                        'allOpenOrders',
                        'listenKey',
                    ],
                },
                'fapiPrivatev2': {
                    'get': [
                        'positionRisk',
                        'account',
                        'balance',
                    ]
                },
                'public': {
                    'get': [
                        'ping',
                        'time',
                        'depth',
                        'trades',
                        'aggTrades',
                        'historicalTrades',
                        'klines',
                        'ticker/24hr',
                        'ticker/price',
                        'ticker/bookTicker',
                        'exchangeInfo',
                    ],
                    'put': ['userDataStream'],
                    'post': ['userDataStream'],
                    'delete': ['userDataStream'],
                },
                'private': {
                    'get': [
                        'allOrderList',  # oco
                        'openOrderList',  # oco
                        'orderList',  # oco
                        'order',
                        'openOrders',
                        'allOrders',
                        'account',
                        'myTrades',
                    ],
                    'post': [
                        'order/oco',
                        'order',
                        'order/test',
                    ],
                    'delete': [
                        'orderList',  # oco
                        'order',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                },
            },
            'commonCurrencies': {
                'BCC': 'BCC',  # kept for backward-compatibility https://github.com/ccxt/ccxt/issues/4848
                'YOYO': 'YOYOW',
            },
            # exchange-specific options
            'options': {
                'fetchTradesMethod': 'publicGetAggTrades',  # publicGetTrades, publicGetHistoricalTrades
                'fetchTickersMethod': 'publicGetTicker24hr',
                'defaultTimeInForce': 'GTC',  # 'GTC' = Good To Cancel(default), 'IOC' = Immediate Or Cancel
                'defaultLimitOrderType': 'limit',  # or 'limit_maker'
                'defaultType': 'spot',  # 'spot', 'future'
                'hasAlreadyAuthenticatedSuccessfully': False,
                'warnOnFetchOpenOrdersWithoutSymbol': True,
                'recvWindow': 5 * 1000,  # 5 sec, binance default
                'timeDifference': 0,  # the difference between system clock and Binance clock
                'adjustForTimeDifference': False,  # controls the adjustment logic upon instantiation
                'parseOrderToPrecision': False,  # force amounts and costs in parseOrder to precision
                'newOrderRespType': {
                    'market': 'FULL',  # 'ACK' for order id, 'RESULT' for full order or 'FULL' for order with fills
                    'limit': 'RESULT',  # we change it from 'ACK' by default to 'RESULT'
                },
            },
            'exceptions': {
                'API key does not exist': AuthenticationError,
                'Order would trigger immediately.': InvalidOrder,
                'Account has insufficient balance for requested action.': InsufficientFunds,
                'Rest API trading is not enabled.': ExchangeNotAvailable,
                "You don't have permission.": PermissionDenied,  # {"msg":"You don't have permission.","success":false}
                'Market is closed.': ExchangeNotAvailable,  # {"code":-1013,"msg":"Market is closed."}
                '-1000': ExchangeNotAvailable,
                # {"code":-1000,"msg":"An unknown error occured while processing the request."}
                '-1013': InvalidOrder,  # createOrder -> 'invalid quantity'/'invalid price'/MIN_NOTIONAL
                '-1021': InvalidNonce,  # 'your time is ahead of server'
                '-1022': AuthenticationError,  # {"code":-1022,"msg":"Signature for self request is not valid."}
                '-1100': InvalidOrder,  # createOrder(symbol, 1, asdf) -> 'Illegal characters found in parameter 'price'
                '-1104': ExchangeError,  # Not all sent parameters were read, read 8 parameters but was sent 9
                '-1128': ExchangeError,  # {"code":-1128,"msg":"Combination of optional parameters invalid."}
                '-2010': ExchangeError,
                # generic error code for createOrder -> 'Account has insufficient balance for requested action.', {"code":-2010,"msg":"Rest API trading is not enabled."}, etc...
                '-2011': OrderNotFound,  # cancelOrder(1, 'BTC/USDT') -> 'UNKNOWN_ORDER'
                '-2013': OrderNotFound,  # fetchOrder(1, 'BTC/USDT') -> 'Order does not exist'
                '-2014': AuthenticationError,  # {"code":-2014, "msg": "API-key format invalid."}
                '-2015': AuthenticationError,  # "Invalid API-key, IP, or permissions for action."
                '-2019': InsufficientFunds,  # {"code":-2019,"msg":"Margin is insufficient."}
                '-4047': ChangeMarginTypeError,
                # {"code":-4047,"msg":"Margin type cannot be changed if there exists open orders."}
                '-4050': InsufficientFunds,  # {"code":-4050,"msg":"Cross balance insufficient."}
                '-4067': ChangePositionError,
                # {"code":-4067,"msg":"Position side cannot be changed if there exists position."}
                '-4068': ChangePositionError,
                # {"code":-4068,"msg":"Position side cannot be changed if there exists position."}
                '-4061': ChangePositionError,
                # {"code":-4061,"msg":"Order's position side does not match user's setting."}
            },
            'ignore_exceptions': {
                '-4059': ExchangeError,  # {"code":-4059,"msg":"No need to change position side."}
                '-4046': ExchangeError,  # {"code":-4046,"msg":"No need to change margin type."}
            },
            'fee_tiers': [
                {
                    'level': 0,
                    'maker': Decimal('0.00020'),
                    'taker': Decimal('0.00040'),
                },
                {
                    'level': 1,
                    'maker': Decimal('0.00016'),
                    'taker': Decimal('0.00040'),
                },
                {
                    'level': 2,
                    'maker': Decimal('0.00014'),
                    'taker': Decimal('0.00035'),
                },
                {
                    'level': 3,
                    'maker': Decimal('0.00012'),
                    'taker': Decimal('0.00032'),
                },
                {
                    'level': 4,
                    'maker': Decimal('0.00010'),
                    'taker': Decimal('0.00030'),
                },
                {
                    'level': 5,
                    'maker': Decimal('0.00008'),
                    'taker': Decimal('0.00027'),
                },
                {
                    'level': 6,
                    'maker': Decimal('0.00006'),
                    'taker': Decimal('0.00025'),
                },
                {
                    'level': 7,
                    'maker': Decimal('0.00004'),
                    'taker': Decimal('0.00022'),
                },
                {
                    'level': 8,
                    'maker': Decimal('0.00002'),
                    'taker': Decimal('0.00020'),
                },
                {
                    'level': 9,
                    'maker': Decimal('0.00000'),
                    'taker': Decimal('0.00017'),
                },
            ]
        })

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        url += '/' + path
        if api == 'wapi':
            url += '.html'
        userDataStream = (path == 'userDataStream') or (path == 'listenKey')
        if path == 'historicalTrades':
            if self.apiKey:
                headers = {
                    'X-MBX-APIKEY': self.apiKey,
                }
            else:
                raise AuthenticationError(self.id + ' historicalTrades endpoint requires `apiKey` credential')
        elif userDataStream:
            if self.apiKey:
                # v1 special case for userDataStream
                body = self.urlencode(params)
                headers = {
                    'X-MBX-APIKEY': self.apiKey,
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            else:
                raise AuthenticationError(self.id + ' userDataStream endpoint requires `apiKey` credential')
        if (api == 'private') or (api == 'sapi') or (api == 'wapi' and path != 'systemStatus') or (
                api == 'fapiPrivate') or (api == 'fapiPrivatev2'):
            self.check_required_credentials()
            query = None
            if (api == 'sapi') and (path == 'asset/dust'):
                query = self.urlencode_with_array_repeat(self.extend({
                    'timestamp': self.nonce(),
                    'recvWindow': self.options['recvWindow'],
                }, params))
            else:
                query = self.urlencode(self.extend({
                    'timestamp': self.nonce(),
                    'recvWindow': self.options['recvWindow'],
                }, params))
            signature = self.hmac(self.encode(query), self.encode(self.secret))
            query += '&' + 'signature=' + signature
            headers = {
                'X-MBX-APIKEY': self.apiKey,
            }
            if (method == 'GET') or (method == 'DELETE') or (api == 'wapi'):
                url += '?' + query
            else:
                body = query
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            # userDataStream endpoints are public, but POST, PUT, DELETE
            # therefore they don't accept URL query arguments
            # https://github.com/ccxt/ccxt/issues/5224
            if not userDataStream:
                if params:
                    url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    async def fetch_markets(self, params=None):
        response = await self.fapiPublicGetExchangeInfo()
        if self.options['adjustForTimeDifference']:
            await self.load_time_difference()
        markets = response['symbols']

        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['symbol']
            baseId = market['baseAsset']
            quoteId = market['quoteAsset']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            filters = self.index_by(market['filters'], 'filterType')
            precision = {
                # 'base': market['baseAssetPrecision'],
                # 'quote': market['quotePrecision'],
                'amount': market['quantityPrecision'],
                'price': market['pricePrecision'],
            }
            active = (market['status'] == 'TRADING')
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': None,
                        'max': None,
                    },
                },
                # 维持保证金比例
                'maintMarginPercent': self.safe_decimal(market, 'maintMarginPercent'),
                # 所需保证金比例
                'requiredMarginPercent': self.safe_decimal(market, 'requiredMarginPercent'),
            }
            # 价格限制
            if 'PRICE_FILTER' in filters:
                filter = filters['PRICE_FILTER']
                entry['limits']['price'] = {
                    'min': self.safe_decimal(filter, 'minPrice'),
                    'max': self.safe_decimal(filter, 'maxPrice'),
                    # 步长
                    'stepSize': self.safe_decimal(filter, 'tickSize'),
                }
            # 数量限制
            if 'LOT_SIZE' in filters:
                filter = filters['LOT_SIZE']
                entry['limits']['amount'] = {
                    'min': self.safe_decimal(filter, 'minQty'),
                    'max': self.safe_decimal(filter, 'maxQty'),
                    # 步长
                    'stepSize': self.safe_decimal(filter, 'stepSize'),
                }
            # 市价订单数量限制
            if 'MARKET_LOT_SIZE' in filters:
                # 字段同数量限制
                pass
            # 价格比限制
            if 'PERCENT_PRICE' in filters:
                # multiplierUp: 价格上限百分比
                # multiplierDown: 价格下限百分比
                pass
            # 最多挂单数限制
            if 'MAX_NUM_ORDERS' in filters:
                # limit
                pass
            result.append(entry)
        return result

    async def fetch_balance(self, params=None):
        response = await self.fapiPrivatev2GetAccount()
        #
        # spot
        #
        #     {
        #         makerCommission: 10,
        #         takerCommission: 10,
        #         buyerCommission: 0,
        #         sellerCommission: 0,
        #         canTrade: True,
        #         canWithdraw: True,
        #         canDeposit: True,
        #         updateTime: 1575357359602,
        #         accountType: "MARGIN",
        #         balances: [
        #             {asset: "BTC", free: "0.00219821", locked: "0.00000000"  },
        #         ]
        #     }
        #
        # futures(fapi)
        #
        #     {
        #     "feeTier": 0,  // 手续费等级
        #     "canTrade": true,  // 是否可以交易
        #     "canDeposit": true,  // 是否可以入金
        #     "canWithdraw": true, // 是否可以出金
        #     "updateTime": 0,
        #     "totalInitialMargin": "0.00000000",  // 但前所需起始保证金总额(存在逐仓请忽略)
        #     "totalMaintMargin": "0.00000000",  // 维持保证金总额
        #     "totalWalletBalance": "23.72469206",   // 账户总余额
        #     "totalUnrealizedProfit": "0.00000000",  // 持仓未实现盈亏总额
        #     "totalMarginBalance": "23.72469206",  // 保证金总余额
        #     "totalPositionInitialMargin": "0.00000000",  // 持仓所需起始保证金(基于最新标记价格)
        #     "totalOpenOrderInitialMargin": "0.00000000",  // 当前挂单所需起始保证金(基于最新标记价格)
        #     "totalCrossWalletBalance": "23.72469206",  // 全仓账户余额
        #     "totalCrossUnPnl": "0.00000000",    // 全仓持仓未实现盈亏总额
        #     "availableBalance": "23.72469206",       // 可用余额
        #     "maxWithdrawAmount": "23.72469206"     // 最大可转出余额
        #     "assets": [
        #         {
        #             "asset": "USDT",        //资产
        #             "walletBalance": "23.72469206",  //余额
        #             "unrealizedProfit": "0.00000000",  // 未实现盈亏
        #             "marginBalance": "23.72469206",  // 保证金余额
        #             "maintMargin": "0.00000000",    // 维持保证金
        #             "initialMargin": "0.00000000",  // 当前所需起始保证金
        #             "positionInitialMargin": "0.00000000",  // 持仓所需起始保证金(基于最新标记价格)
        #             "openOrderInitialMargin": "0.00000000", // 当前挂单所需起始保证金(基于最新标记价格)
        #             "crossWalletBalance": "23.72469206",  //全仓账户余额
        #             "crossUnPnl": "0.00000000" // 全仓持仓未实现盈亏
        #             "availableBalance": "23.72469206",       // 可用余额
        #             "maxWithdrawAmount": "23.72469206"     // 最大可转出余额
        #         }
        #     ],
        #     "positions": [  // 头寸，将返回所有市场symbol。
        #         //根据用户持仓模式展示持仓方向，即双向模式下只返回BOTH持仓情况，单向模式下只返回 LONG 和 SHORT 持仓情况
        #         {
        #             "symbol": "BTCUSDT",  // 交易对
        #             "initialMargin": "0",   // 当前所需起始保证金(基于最新标记价格)
        #             "maintMargin": "0", //维持保证金
        #             "unrealizedProfit": "0.00000000",  // 持仓未实现盈亏
        #             "positionInitialMargin": "0",  // 持仓所需起始保证金(基于最新标记价格)
        #             "openOrderInitialMargin": "0",  // 当前挂单所需起始保证金(基于最新标记价格)
        #             "leverage": "100",  // 杠杆倍率
        #             "isolated": true,  // 是否是逐仓模式
        #             "entryPrice": "0.00000",  // 持仓成本价
        #             "maxNotional": "250000",  // 当前杠杆下用户可用的最大名义价值
        #             "positionSide": "BOTH"  // 持仓方向。
        #         }
        #     ]
        # }
        #

        result = {'info': response, 'currencies': {}}
        balances = self.safe_value(response, 'assets', [])
        for balance in balances:
            currencyId = self.safe_string(balance, 'asset')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_decimal(balance, 'availableBalance')
            account['total'] = self.safe_decimal(balance, 'walletBalance')
            account['used'] = account['total'] - account['free']
            result['currencies'][code] = account
        result['totalInitialMargin'] = self.safe_decimal(response, 'totalInitialMargin')
        result['totalMaintMargin'] = self.safe_decimal(response, 'totalMaintMargin')
        result['totalWalletBalance'] = self.safe_decimal(response, 'totalWalletBalance')
        result['totalUnrealizedProfit'] = self.safe_decimal(response, 'totalUnrealizedProfit')
        result['totalMarginBalance'] = self.safe_decimal(response, 'totalMarginBalance')
        result['totalPositionInitialMargin'] = self.safe_decimal(response, 'totalPositionInitialMargin')
        result['totalOpenOrderInitialMargin'] = self.safe_decimal(response, 'totalOpenOrderInitialMargin')
        result['totalCrossWalletBalance'] = self.safe_decimal(response, 'totalCrossWalletBalance')
        result['totalCrossUnPnl'] = self.safe_decimal(response, 'totalCrossUnPnl')
        result['availableBalance'] = self.safe_decimal(response, 'availableBalance')
        result['maxWithdrawAmount'] = self.safe_decimal(response, 'maxWithdrawAmount')

        return result

    async def fetch_order_book(self, symbol, limit=None, params=None):
        await self.load_markets()
        market = self.market(symbol)

        request = {'symbol': market['id']}
        if limit is not None:
            # default 100, max 5000
            request['limit'] = min(int(limit), 5000)
        response = await self.fapiPublicGetDepth(self.extend(request, params))

        orderbook = self.parse_order_book(response)
        orderbook['nonce'] = self.safe_integer(response, 'lastUpdateId')
        return orderbook

    async def create_order(self, symbol, type, side, amount=None, price=None, clientOrderId=None, positionSide=None, reduceOnly=False, params=None):
        await self.load_markets()
        market = self.market(symbol)

        amount = amount and self.amount_to_precision(symbol, amount)
        price = price and self.price_to_precision(symbol, price)

        uppercaseType = type.upper()
        request = {
            'symbol': market['id'],
            'type': uppercaseType,
            'side': side.upper(),
        }

        newClientOrderId = self.client_order_id(clientOrderId)
        request['newClientOrderId'] = newClientOrderId

        if uppercaseType == 'MARKET':
            quoteOrderQty = self.safe_decimal(params, 'quoteOrderQty')
            if quoteOrderQty is not None:
                request['quoteOrderQty'] = quoteOrderQty
                params = self.omit(params, 'quoteOrderQty')
            else:
                request['quantity'] = amount
        else:
            request['quantity'] = amount
        timeInForceIsRequired = False
        priceIsRequired = False
        stopPriceIsRequired = False
        if uppercaseType == 'LIMIT':
            priceIsRequired = True
            timeInForceIsRequired = True
        elif (uppercaseType == 'STOP_LOSS') or (uppercaseType == 'TAKE_PROFIT'):
            stopPriceIsRequired = True
            priceIsRequired = True
        elif (uppercaseType == 'STOP_LOSS_LIMIT') or (uppercaseType == 'TAKE_PROFIT_LIMIT'):
            stopPriceIsRequired = True
            priceIsRequired = True
            timeInForceIsRequired = True
        elif uppercaseType == 'LIMIT_MAKER':
            priceIsRequired = True
        elif uppercaseType == 'STOP':
            stopPriceIsRequired = True
            priceIsRequired = True
        if priceIsRequired:
            if price is None:
                raise InvalidOrder(
                    self.id + ' createSwapOrder method requires a price argument for a ' + type + ' order')
            request['price'] = price
        if timeInForceIsRequired:
            request['timeInForce'] = self.options[
                'defaultTimeInForce']  # 'GTC' = Good To Cancel(default), 'IOC' = Immediate Or Cancel
        if stopPriceIsRequired:
            stopPrice = self.safe_decimal(params, 'stopPrice')
            if stopPrice is None:
                raise InvalidOrder(
                    self.id + ' createSwapOrder method requires a stopPrice extra param for a ' + type + ' order')
            else:
                params = self.omit(params, 'stopPrice')
                request['stopPrice'] = stopPrice

        if positionSide:
            request['positionSide'] = positionSide.upper()

        if reduceOnly is not None:
            request['reduceOnly'] = reduceOnly

        response = await self.fapiPrivatePostOrder(self.extend(request, params))
        return self.parse_swap_order(response, market)

    async def cancel_order(self, id, symbol, clientOrderId=None, params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
            # 'orderId': int(id),
            # 'origClientOrderId': id,
        }

        origClientOrderId = clientOrderId
        if origClientOrderId is not None:
            request['origClientOrderId'] = origClientOrderId
        else:
            request['orderId'] = int(id)

        response = await self.fapiPrivateDeleteOrder(self.extend(request, params))
        return {
            'info': response
        }

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, fromId=None, direct='next', params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetch_open_orders requires a symbol argument')

        await self.load_markets()
        market = self.market(symbol)

        if direct is not None and direct != 'next':
            raise ArgumentsRequired('in binance "direct" can only be next')

        request = {}
        if symbol is not None:
            request['symbol'] = market['id']

        if fromId is not None:
            request['orderId'] = fromId
        response = await self.fapiPrivateGetOpenOrders(self.extend(request, params))

        return self.parse_orders(response, market, since, limit)

    async def fetch_closed_orders(self, symbol, since=None, limit=None, fromId=None, direct='next', params=None):
        orders = await self.fetch_orders(symbol, since, limit, fromId, direct, params)
        return self.filter_by_array(orders, 'status', values={'closed', 'canceled', 'canceling'}, indexed=False)

    async def fetch_order(self, id=None, symbol=None, clientOrderId=None, params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
        }
        origClientOrderId = clientOrderId
        if origClientOrderId is not None:
            request['origClientOrderId'] = origClientOrderId
        else:
            request['orderId'] = int(id)
        response = await self.fapiPrivateGetOrder(self.extend(request, params))

        return self.parse_swap_order(response, market)

    async def fetch_orders(self, symbol, since=None, limit=None, fromId=None, direct='next', params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')

        if direct is not None and direct != 'next':
            raise ArgumentsRequired('in binance "direct" can only be next')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            # 默认值 500; 最大值 1000
            request['limit'] = min(int(limit), 1000)

        if fromId is not None:
            request['orderId'] = fromId
        response = await self.fapiPrivateGetAllOrders(self.extend(request, params))

        return self.parse_swap_orders(response, market, since, limit)

    async def fetch_my_trades(self, symbol, since=None, limit=None, fromId=None, direct='next', params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades requires a symbol argument')

        if direct is not None and direct != 'next':
            raise ArgumentsRequired('in binance "direct" can only be next')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        if fromId is not None:
            try:
                params['fromId'] = int(fromId)
            except (TypeError, ValueError):
                raise BadRequest(self.id + f' fetchMyTrades invalid fromId: {fromId}')

        response = await self.fapiPrivateGetUserTrades(self.extend(request, params))
        return self.parse_swap_trades(response, market)

    async def change_leverage(self, symbol, leverage, positionSide=None, params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' swapLeverage requires a symbol argument')

        try:
            leverage = int(leverage)
        except (TypeError, ValueError):
            raise BadRequest(f'swapLeverage invalid leverage: {leverage}')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
            # 目标杠杆倍数：1 到 125 整数
            'leverage': leverage,
        }

        response = await self.fapiPrivatePostLeverage(self.extend(request, params))
        return {
            'info': response,
        }

    async def change_margin_type(self, symbol, marginType, positionSide=None, params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' swapMarginType requires a symbol argument')

        margin_type = marginType.upper()
        if margin_type not in {'ISOLATED', 'CROSSED'}:
            raise BadRequest(f'swapMarginType invalid type: {margin_type}')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
            'marginType': margin_type,
        }

        response = await self.fapiPrivatePostMarginType(self.extend(request, params))
        return {
            'info': response,
        }

    async def change_isolated_margin(self, symbol, positionSide, direction, amount, params=None):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' swapPositionMargin requires a symbol argument')

        direction = direction.upper()
        if direction not in {'ASC', 'DESC'}:
            raise BadRequest(f'swapPositionMargin invalid type: {direction}')

        await self.load_markets()
        market = self.market(symbol)

        request = {
            'symbol': market['id'],
            'amount': Decimal(amount),
            'type': 1 if 'ASC' == direction.upper() else 2,
        }

        if positionSide:
            request['positionSide'] = positionSide.upper()

        response = await self.fapiPrivatePostPositionMargin(self.extend(request, params))

        return {
            'info': response
        }

    async def change_position_side(self, symbol, positionSide, params=None):

        request = {'dualSidePosition': 'true' if positionSide == 'dual' else 'false'}
        response = await self.fapiPrivatePostPositionSideDual(self.extend(request, params))

        return {
            'info': response,
        }

    async def fetch_trading_fee_rates(self, symbol=None, params=None):
        response = await self.fapiPrivateGetAccount(params)
        fee_tier = response.get('feeTier')
        fee_tier = self.fee_tiers[int(fee_tier)]
        return [{
            'symbol': None,
            'maker': fee_tier['maker'],
            'taker': fee_tier['taker'],
            'info': response
        }]

    async def fetch_position_side(self, symbol=None, params=None):
        response = await self.fapiPrivateGetPositionSideDual(params)

        return {
            'info': response,
            'positionSide': 'dual' if response.get('dualSidePosition') else 'single'
        }

    async def fetch_funding_records(self, symbol=None, since=None, limit=None, fromId=None, direct='next', params=None):
        request = {}

        if symbol is not None:
            await self.load_markets()
            market = self.market(symbol)

            request['symbol'] = market['id']

        request['incomeType'] = 'FUNDING_FEE'
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.fapiPrivateGetIncome(self.extend(request, params))
        return self.parse_funding_fees(response)

    async def fetch_positions(self, symbol=None, params=None):
        await self.load_markets()

        response = await self.fapiPrivatev2GetPositionRisk(params)
        return self.parse_swap_positions(response, symbol)

    def parse_swap_order_status(self, status):
        statuses = {
            'NEW': 'open',
            'PARTIALLY_FILLED': 'open',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
            'PENDING_CANCEL': 'canceling',  # currently unused
            'REJECTED': 'rejected',
            'EXPIRED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    async def fetch_incomes(self, symbol=None, since=None, limit=None, fromId=None, direct='next', params=None):
        request = {}
        await self.load_markets()

        if symbol is not None:
            market = self.market(symbol)

            request['symbol'] = market['id']
        if 'incomeType' in params:
            income_type = params.pop('incomeType').upper()
            if income_type not in {'TRANSFER', 'WELCOME_BONUS', 'REALIZED_PNL',
                                   'FUNDING_FEE', 'COMMISSION', 'INSURANCE_CLEAR'}:
                raise BadRequest(f'fetchSwapIncome invalid incomeType: {income_type}')
            request['incomeType'] = income_type
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.fapiPrivateGetIncome(self.extend(request, params))
        return self.parse_swap_incomes(response)

    def parse_funding_fee(self, result):

        return {
            'id': None,
            'fundingFee': self.safe_decimal(result, 'income'),
            'position': None,
            'positionValue': None,
            'fundingRate': None,
            'timestamp': self.safe_integer(result, 'time'),
            'info': {}
        }

    def parse_swap_order(self, order, market=None):
        #
        #  spot
        #
        #     {
        #         "symbol": "LTCBTC",
        #         "orderId": 1,
        #         "clientOrderId": "myOrder1",
        #         "price": "0.1",
        #         "origQty": "1.0",
        #         "executedQty": "0.0",
        #         "cummulativeQuoteQty": "0.0",
        #         "status": "NEW",
        #         "timeInForce": "GTC",
        #         "type": "LIMIT",
        #         "side": "BUY",
        #         "stopPrice": "0.0",
        #         "icebergQty": "0.0",
        #         "time": 1499827319559,
        #         "updateTime": 1499827319559,
        #         "isWorking": True
        #     }
        #
        #  futures
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "orderId": 1,
        #         "clientOrderId": "myOrder1",
        #         "price": "0.1",
        #         "origQty": "1.0",
        #         "executedQty": "1.0",
        #         "cumQuote": "10.0",
        #         "status": "NEW",
        #         "timeInForce": "GTC",
        #         "type": "LIMIT",
        #         "side": "BUY",
        #         "stopPrice": "0.0",
        #         "updateTime": 1499827319559
        #     }
        #
        status = self.parse_swap_order_status(self.safe_string(order, 'status'))
        symbol = None
        marketId = self.safe_string(order, 'symbol')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = None
        if 'time' in order:
            timestamp = self.safe_integer(order, 'time')
        elif 'transactTime' in order:
            timestamp = self.safe_integer(order, 'transactTime')
        price = self.safe_decimal(order, 'price')
        amount = self.safe_decimal(order, 'origQty')
        filled = self.safe_decimal(order, 'executedQty')
        remaining = None
        # - Spot/Margin market: cummulativeQuoteQty
        # - Futures market: cumQuote.
        #   Note self is not the actual cost, since Binance futures uses leverage to calculate margins.
        cost = self.safe_decimal_2(order, 'cummulativeQuoteQty', 'cumQuote')
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
                if self.options['parseOrderToPrecision']:
                    remaining = Decimal(self.amount_to_precision(symbol, remaining))
                remaining = max(remaining, 0.0)
            if price is not None:
                if cost is None:
                    cost = price * filled
        id = self.safe_string(order, 'orderId')
        type = self.safe_string(order, 'type').lower()
        if type == 'market':
            if price == 0.0:
                if (cost is not None) and (filled is not None):
                    if (cost > 0) and (filled > 0):
                        price = cost / filled
                        if self.options['parseOrderToPrecision']:
                            price = Decimal(self.price_to_precision(symbol, price))
        elif type == 'limit_maker':
            type = 'limit'
        side = self.safe_string(order, 'side').lower()
        fee = None
        trades = None
        fills = self.safe_value(order, 'fills')
        if fills is not None:
            trades = self.parse_trades(fills, market)
            numTrades = len(trades)
            if numTrades > 0:
                cost = trades[0]['cost']
                fee = {
                    'cost': trades[0]['fee']['cost'],
                    'currency': trades[0]['fee']['currency'],
                }
                for i in range(1, len(trades)):
                    cost = self.sum(cost, trades[i]['cost'])
                    fee['cost'] = self.sum(fee['cost'], trades[i]['fee']['cost'])
        average = None
        if cost is not None:
            if filled:
                average = cost / filled
                if self.options['parseOrderToPrecision']:
                    average = Decimal(self.price_to_precision(symbol, average))
            if self.options['parseOrderToPrecision']:
                cost = Decimal(self.cost_to_precision(symbol, cost))
        clientOrderId = self.safe_string(order, 'clientOrderId')
        lastTradeTimestamp = self.safe_string(order, 'updateTime')
        timestamp = timestamp or lastTradeTimestamp
        return {
            'info': order,
            'id': id,
            'client_order_id': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
            'positionSide': self.safe_string(order, 'positionSide'),
            'realizedPnl': self.safe_decimal(order, 'realizedPnl')
        }

    def parse_swap_trade(self, trade, market=None):
        # futures trades
        # https://binance-docs.github.io/apidocs/futures/en/#user_data-8
        #
        #     {
        #         "buyer": false, // 是否是买方
        #         "commission": "-0.07819010", // 手续费
        #         "commissionAsset": "USDT", // 手续费计价单位
        #         "id": 698759, // 交易ID
        #         "maker": false, // 是否是挂单方
        #         "orderId": 25851813, // 订单编号
        #         "price": "7819.01", // 成交价
        #         "qty": "0.002", // 成交数量
        #         "quoteQty": "15.63802", // 成交额
        #         "realizedPnl": "-0.91539999", // 实现盈亏
        #         "side": "SELL", // 买卖方向
        #         "positionSide": "SHORT", // 持仓方向
        #         "symbol": "BTCUSDT", // 交易对
        #         "time": 1569514978020 // 时间
        #     }
        timestamp = self.safe_integer_2(trade, 'T', 'time')
        price = self.safe_decimal_2(trade, 'p', 'price')
        amount = self.safe_decimal_2(trade, 'q', 'qty')
        id = self.safe_string_2(trade, 'a', 'id')
        side = None
        orderId = self.safe_string(trade, 'orderId')
        if 'm' in trade:
            side = 'sell' if trade['m'] else 'buy'  # self is reversed intentionally
        elif 'isBuyerMaker' in trade:
            side = 'sell' if trade['isBuyerMaker'] else 'buy'
        elif 'side' in trade:
            side = self.safe_string(trade, 'side').upper()
        else:
            if 'isBuyer' in trade:
                side = 'buy' if trade['isBuyer'] else 'sell'  # self is a True side
        fee = None
        if 'commission' in trade:
            fee = {
                'cost': self.safe_decimal(trade, 'commission'),
                'currency': self.safe_currency_code(self.safe_string(trade, 'commissionAsset')),
            }
        takerOrMaker = None
        if 'isMaker' in trade:
            takerOrMaker = 'maker' if trade['isMaker'] else 'taker'
        if 'maker' in trade:
            takerOrMaker = 'maker' if trade['maker'] else 'taker'
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'symbol')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': None,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': price * amount,
            'fee': fee,
            'positionSide': self.safe_string(trade, 'positionSide'),
            'realizedPnl': self.safe_decimal(trade, 'realizedPnl')
        }

    def parse_swap_orders(self, orders, market=None, since=None, limit=None, params={}):
        array = self.to_array(orders)
        array = [self.extend(self.parse_swap_order(order, market), params) for order in array]
        array = self.sort_by(array, 'timestamp')
        symbol = market['symbol'] if market else None
        return self.filter_by_symbol_since_limit(array, symbol, since, limit)

    def parse_swap_trades(self, trades, market=None, since=None, limit=None, params={}):
        array = self.to_array(trades)
        array = [self.extend(self.parse_swap_trade(trade, market), params) for trade in array]
        array = self.sort_by(array, 'timestamp')
        symbol = market['symbol'] if market else None
        return self.filter_by_symbol_since_limit(array, symbol, since, limit)

    def parse_funding_fees(self, fees, params={}):
        array = self.to_array(fees)
        array = [self.extend(self.parse_funding_fee(fee), params) for fee in array]
        array = self.sort_by(array, 'timestamp')
        return array

    def parse_swap_positions(self, response, symbol, params={}):
        array = self.to_array(response)
        array = [self.extend(self.parse_swap_position(position), params) for position in array]
        return self.filter_by_symbol(array, symbol)

    def parse_swap_position(self, position):
        symbol = None
        market = None
        marketId = self.safe_string(position, 'symbol')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']

        return {
            'info': position,
            'symbol': symbol,
            'position': self.safe_string(position, 'positionAmt'),
            'openPrice': self.safe_string(position, 'entryPrice'),
            'markPrice': self.safe_string(position, 'markPrice'),
            'unrealizedProfit': self.safe_string(position, 'unRealizedProfit'),
            'liquidatePrice': self.safe_string(position, 'liquidationPrice'),
            'leverage': self.safe_integer(position, 'leverage'),
            'marginType': self.safe_string(position, 'marginType'),
            'initMargin': self.truncate_to_string(
                self.safe_decimal(position, 'isolatedMargin') - self.safe_decimal(position, 'unRealizedProfit'), 8),
            'positionSide': self.safe_string(position, 'positionSide'),
        }

    def parse_swap_income(self, income):
        symbol = None
        market = None
        marketId = self.safe_string(income, 'symbol')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']

        return {
            "symbol": symbol,
            "incomeType": income['incomeType'],
            "income": income['income'],
            "asset": income['asset'],
            'time': income['time'],
            "tranId": income['tranId'],
            "tradeId": income['tradeId'],
            "info": income
        }

    def parse_swap_incomes(self, incomes, params=None):
        array = self.to_array(incomes)
        array = [self.extend(self.parse_swap_income(income), params) for income in array]
        array = self.sort_by(array, 'timestamp')
        return array

    def handle_rest_errors(self, exception, http_status_code, response, url, method='GET'):
        if response:
            for error in self.ignore_exceptions:
                if error in response:
                    return
        super().handle_rest_errors(exception, http_status_code, response, url, method)

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if (code == 418) or (code == 429):
            raise DDoSProtection(self.id + ' ' + str(code) + ' ' + reason + ' ' + body)
        # error response in a form: {"code": -1013, "msg": "Invalid quantity."}
        # following block cointains legacy checks against message patterns in "msg" property
        # will switch "code" checks eventually, when we know all of them
        if code >= 400:
            if body.find('Price * QTY is zero or less') >= 0:
                raise InvalidOrder(self.id + ' order cost = amount * price is zero or less ' + body)
            if body.find('LOT_SIZE') >= 0:
                raise InvalidOrder(self.id + ' order amount should be evenly divisible by lot size ' + body)
            if body.find('PRICE_FILTER') >= 0:
                raise InvalidOrder(self.id + ' order price is invalid, i.e. exceeds allowed price precision, exceeds min price or max price limits or is invalid float value in general, use self.price_to_precision(symbol, amount) ' + body)
        if response is None:
            return  # fallback to default error handler
        # check success value for wapi endpoints
        # response in format {'msg': 'The coin does not exist.', 'success': True/false}
        success = self.safe_value(response, 'success', True)
        if not success:
            message = self.safe_string(response, 'msg')
            parsedMessage = None
            if message is not None:
                try:
                    parsedMessage = json.loads(message)
                except Exception as e:
                    # do nothing
                    parsedMessage = None
                if parsedMessage is not None:
                    response = parsedMessage
        message = self.safe_string(response, 'msg')
        if message is not None:
            self.throw_exactly_matched_exception(self.exceptions, message, self.id + ' ' + message)
        # checks against error codes
        error = self.safe_string(response, 'code')
        if error is not None:
            # https://github.com/ccxt/ccxt/issues/6501
            if error == '200':
                return
            # a workaround for {"code":-2015,"msg":"Invalid API-key, IP, or permissions for action."}
            # despite that their message is very confusing, it is raised by Binance
            # on a temporary ban, the API key is valid, but disabled for a while
            if (error == '-2015') and self.options['hasAlreadyAuthenticatedSuccessfully']:
                raise DDoSProtection(self.id + ' temporary banned: ' + body)
            feedback = self.id + ' ' + body
            self.throw_exactly_matched_exception(self.exceptions, error, feedback)
            if error not in self.ignore_exceptions:
                raise ExchangeError(feedback)
        if not success:
            raise ExchangeError(self.id + ' ' + body)

    def client_order_id(self, origin_client_order_id, prefix='x-VULwwsN3'):
        if not origin_client_order_id:
            uuid = self.uuid().replace('-', '')
            buffer = [_a ^ _b for _a, _b in zip(bytes.fromhex(uuid[:16]), bytes.fromhex(uuid[-16:]))]
            origin_client_order_id = bytes(buffer).hex()
            origin_client_order_id = origin_client_order_id.upper()

        if not origin_client_order_id.startswith(prefix):
            origin_client_order_id = prefix + origin_client_order_id
        return origin_client_order_id
