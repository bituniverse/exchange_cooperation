class SwapApi:
    # API definition for Perpetual Contract Trading

    """
      Server time
    """

    async def fetch_time(self, params={}):
        """
            fetch_markets
        """

    async def fetch_markets(self, params={}):
        raise NotImplementedError()

    """
      fetch_markets_by_type
    """

    async def fetch_markets_by_type(self, type, params={}):
        raise NotImplementedError()

    """
       fetch_order_book
    """

    async def fetch_order_book(self, symbol, params={}):
        raise NotImplementedError()

    """
       fetch_ticker
    """

    async def fetch_ticker(self, symbol, params={}):
        raise NotImplementedError()

    """ 
       fetch_tickers
    """

    async def fetch_tickers(self, symbols=None, params={}):
        raise NotImplementedError()

    """
      fetch_trades
    """

    async def fetch_trades(self, symbol, limit=None, since=None, params={}):
        raise NotImplementedError()

    """
      fetch_ohlcv
    """

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        raise NotImplementedError()

    """
         fetch_balance
    """

    async def fetch_balance(self, params={}):
        raise NotImplementedError()

    """
       create_order
    """

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        raise NotImplementedError()

    """
      cancel_order
    """

    async def cancel_order(self, id, symbol=None, clientOrderId=None,params={}):
        raise NotImplementedError()

    """

      cancel_orders
    """

    async def cancel_orders(self, ids, symbol=None, params={}):
        raise NotImplementedError()

    """
      fetch_order
    """

    async def fetch_order(self, id, symbol=None,clientOrderId=None, params={}):
        raise NotImplementedError()

    """
      fetch_open_orders
    """

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        raise NotImplementedError()

    """
       fetch_closed_orders
    """

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        raise NotImplementedError()

    """
       fetch_order_trades
    """

    async def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        raise NotImplementedError()

    """
     symbol   CMT_BTCUSDT
     since    None
     limit    None
     fromId   None
     direct   None
     params={"from":"1","to":"1","limit":"100","status":"5"}
    """

    async  def fetch_orders(self, symbol, since=None, limit=None, fromId=None, direct='next', params=None):
        raise NotImplementedError()

    """
     symbol  None
     params  None
    """

    async def fetch_trading_fee_rates(self, symbol=None, params=None):
        raise NotImplementedError()

    """
     symbol   None
     params   None
    """

    async def fetch_positions(self, symbol=None, params=None):
        raise NotImplementedError()

    """
      symbol  CMT_BTCUSDT
      leverage 10
      positionSide None
      params={"holdSide":2}
    """

    async def change_leverage(self, symbol, leverage, positionSide=None, params=None):
        raise NotImplementedError()

    """
     symbol  CMT_BTCUSDT
     marginType None
     positionSide None
     params={"holdModel":1}
    """

    async def change_margin_type(self, symbol, marginType, positionSide=None, params=None):
        raise NotImplementedError()

    """
    symbol  CMT_BTCUSDT
    params  None
    
    """

    async def fetch_position_side(self, symbol=None, params=None):
        raise NotImplementedError()

    """
    symbol    CMT_BTCUSDT
    since     None
    limit     None
    fromId    None
    direct    None
    params={"pageIndex":1,"pageSize":50}
    
    """

    async def fetch_funding_records(self, symbol=None, since=None, limit=None, fromId=None, direct='next', params=None):
        raise NotImplementedError()

    """
    symbol    CMT_BTCUSDT
    positionSide None
    direction    None
    amount       10 
    params={"positionType":1,"type":1}
    """

    async def change_isolated_margin(self, symbol, positionSide, direction, amount, params=None):
        raise NotImplementedError()



