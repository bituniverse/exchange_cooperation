from datetime import datetime
from decimal import Decimal

from schema import Schema, Or, Optional, And, Use


def is_millisecond_timestamp(timestamp):
    seconds_datetime = datetime.fromtimestamp(int(timestamp) / 1000)

    try:
        milliseconds_datetime = datetime.fromtimestamp(timestamp)
        now = datetime.now()
        return abs((now - milliseconds_datetime).seconds) > abs((now - seconds_datetime).seconds)
    except ValueError:
        return True


NULLABLE_NUMBER = Or(Decimal, float, int, And(str, Use(Decimal)), None)
NUMBER = Or(Decimal, float, int, And(str, Use(Decimal)))
NULLABLE_INT = Or(int, None)
TIMESTAMP = And(Use(int), is_millisecond_timestamp)

MIN_MAX_SCHEMA = Schema(
    {
        'min': NUMBER,
        Optional('max'): NULLABLE_NUMBER,
        Optional('stepSize'): NULLABLE_NUMBER,
    }
)

NULLABLE_MIN_MAX_SCHEMA = Schema(
    {
        Optional('min'): NULLABLE_NUMBER,
        Optional('max'): NULLABLE_NUMBER,
        Optional('stepSize'): NULLABLE_NUMBER,
    }
)

MARKET_SCHEMA = Schema(
    {
        'id': Or(str, int),
        'symbol': str,
        'base': str,
        'quote': str,
        'baseId': str,
        'quoteId': str,
        'active': bool,
        Optional('taker'): NULLABLE_NUMBER,
        Optional('maker'): NULLABLE_NUMBER,
        Optional('percentage'): bool,
        Optional('tierBased'): bool,
        'precision': {
            'price': NUMBER,
            'amount': NUMBER,
            Optional('cost'): NULLABLE_MIN_MAX_SCHEMA,
            Optional(str): object,
        },
        'limits': {
            'amount': MIN_MAX_SCHEMA,
            Optional('price'): Optional(NULLABLE_MIN_MAX_SCHEMA),
            Optional('cost'): Optional(NULLABLE_MIN_MAX_SCHEMA),
            Optional(str): object,
        },
        Optional('info'): object,
        Optional(str): object,
    }
)

MARKETS_SCHEMA = Schema([MARKET_SCHEMA])

ORDER_BOOK_ITEM_SCHEMA = And([NUMBER], lambda x: len(x) == 2)
ORDER_BOOK_SCHEMA = Schema(
    {
        'bids': And([ORDER_BOOK_ITEM_SCHEMA], lambda x: len(x) > 0),
        'asks': And([ORDER_BOOK_ITEM_SCHEMA], lambda x: len(x) > 0),
        Optional('timestamp'): Or(TIMESTAMP, None),
        Optional('datetime'): Or(str, None),
        Optional('nonce'): Or(int, None),
        Optional('info'): object,
        Optional(str): object,
    }
)

FEE_SCHEMA = Schema(
    {
        'cost': NULLABLE_NUMBER,
        'currency': Or(str, None),
        Optional('rate'): NULLABLE_NUMBER
    }
)

TRADE_SCHEMA = Schema(
    {
        'id': Or(str, int),
        Optional('datetime'): Or(str, None),
        'timestamp': TIMESTAMP,
        'symbol': str,
        'order': Or(str, int),
        Optional('type'): Or(str, None),
        'side': str,
        Optional('takerOrMaker'): str,
        'price': NUMBER,
        'amount': NUMBER,
        'cost': NUMBER,
        Optional('fee'): Or(FEE_SCHEMA, None),
        'info': object,
        Optional(str): object,
    }
)

ORDER_SCHEMA = Schema(
    {
        'id': Or(str, int),
        Optional('clientOrderId'): Or(int, str, None),
        Optional('datetime'): Or(str, None),
        'timestamp': TIMESTAMP,
        Optional('lastTradeTimestamp'): Or(TIMESTAMP, None),
        'status': str,
        'symbol': str,
        'type': str,
        'side': str,
        Optional('price'): NULLABLE_NUMBER,
        Optional('average'): NULLABLE_NUMBER,
        'amount': NULLABLE_NUMBER,
        Optional('filled'): NULLABLE_NUMBER,
        Optional('remaining'): NULLABLE_NUMBER,
        Optional('cost'): NULLABLE_NUMBER,
        Optional('trades'): Or([TRADE_SCHEMA], None),
        Optional('fee'): Or(FEE_SCHEMA, None),
        'info': object,
        Optional(str): object,
    }
)

ORDERS_SCHEMA = Schema([ORDER_SCHEMA])

TRADES_SCHEMA = Schema([TRADE_SCHEMA])

INFO_ONLY = Schema(
    {
        'info': object
    }
)

BALANCE_COIN_SCHEMA = Schema(
    {
        str: NUMBER
    }
)

BALANCE_ITEM = Schema(
    {
        'free': NUMBER,
        'used': NUMBER,
        'total': NUMBER,
    }
)

BALANCE_SCHEMA = Schema(
    {
        'free': BALANCE_COIN_SCHEMA,
        'used': BALANCE_COIN_SCHEMA,
        'total': BALANCE_COIN_SCHEMA,
        'info': object,
        str: BALANCE_ITEM
    }
)

FEE_RATE_SCHEMA = Schema(
    {
        Optional('symbol'): Or(str, None),
        'taker': NUMBER,
        'maker': NUMBER,
        Optional('info'): object,

    }
)

FEE_RATES_SCHEMA = Schema([FEE_RATE_SCHEMA])

POSITION_SCHEMA = Schema(
    {
        'symbol': str,
        'position': NUMBER,
        'openPrice': NUMBER,
        Optional('markPrice'): NULLABLE_NUMBER,
        Optional('unrealizedProfit'): NULLABLE_NUMBER,
        Optional('liquidatePrice'): NULLABLE_NUMBER,
        Optional('leverage'): Or(int, None),
        Optional('marginType'): Or(str, None),
        'initMargin': NUMBER,
        Optional('positionSide'): Or(str, None),
        'info': object,
        Optional(str): object,
    }
)

POSITIONS_SCHEMA = Schema([POSITION_SCHEMA])

POSITION_SIDE_SCHEMA = Schema({
    Optional('symbol'): Or(str, None),
    'positionSide': str,
    'info': object,
})

FUNDING_FEE_SCHEMA = Schema({
    Optional('id'): Or(str, int, None),
    'fundingFee': NUMBER,
    Optional('position'): NULLABLE_NUMBER,
    Optional('positionValue'): NULLABLE_NUMBER,
    Optional('fundingRate'): NULLABLE_NUMBER,
    'timestamp': TIMESTAMP,
    'info': object,
    Optional(str): object,
})

FUNDING_FEEs_SCHEMA = Schema([FUNDING_FEE_SCHEMA])
