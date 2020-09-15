class SwapApi:
    # API definition for Perpetual Contract Trading

    """
      Server time
    """

    def fetch_time(self, params={}):
        """
            fetch_markets
        """

    def fetch_markets(self, params={}):
        raise NotImplementedError()

    """
      fetch_markets_by_type
    """

    def fetch_markets_by_type(self, type, params={}):
        raise NotImplementedError()

    """
       fetch_order_book
    """

    def fetch_order_book(self, symbol, params={}):
        raise NotImplementedError()

    """
       fetch_ticker
    """

    def fetch_ticker(self, symbol, params={}):
        raise NotImplementedError()

    """ 
       fetch_tickers
    """

    def fetch_tickers(self, symbols=None, params={}):
        raise NotImplementedError()

    """
      fetch_trades
    """

    def fetch_trades(self, symbol, limit=None, since=None, params={}):
        raise NotImplementedError()

    """
      fetch_ohlcv
    """

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        raise NotImplementedError()

    """
         fetch_balance
    """

    def fetch_balance(self, params={}):
        raise NotImplementedError()

    """
       create_order
    """

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        raise NotImplementedError()

    """
      cancel_order
    """

    def cancel_order(self, id, symbol=None, params={}):
        raise NotImplementedError()

    """

      cancel_orders
    """

    def cancel_orders(self, ids, symbol=None, params={}):
        raise NotImplementedError()

    """
      fetch_order
    """

    def fetch_order(self, id, symbol=None, params={}):
        raise NotImplementedError()

    """
      fetch_open_orders
    """

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        raise NotImplementedError()

    """
       fetch_closed_orders
    """

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        raise NotImplementedError()

    """
       fetch_order_trades
    """

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        raise NotImplementedError()

    """
     symbol 
     limit
     params={"status":2,"from":"2","to":2}
    """

    def fetch_orders(self, symbol, since=None, limit=None, fromId=None, direct='next', params=None):
        raise NotImplementedError()

    """

    """

    def fetch_trading_fee_rates(self, symbol=None, params=None):
        raise NotImplementedError()

    """

    """

    def fetch_positions(self, symbol=None, params=None):
        raise NotImplementedError()

    """
    """

    def change_leverage(self, symbol, leverage, positionSide=None, params=None):
        raise NotImplementedError()

    """
    """

    def change_margin_type(self, symbol, marginType, positionSide=None, params=None):
        raise NotImplementedError()

    """
    """

    def fetch_position_side(self, symbol=None, params=None):
        raise NotImplementedError()

    """
    """

    def fetch_funding_records(self, symbol=None, since=None, limit=None, fromId=None, direct='next', params=None):
        raise NotImplementedError()

    """
    """

    def change_isolated_margin(self, symbol, positionSide, direction, amount, params=None):
        raise NotImplementedError()

    """
    """

    def fetch_incomes(self, symbol=None, since=None, limit=None, fromId=None, direct='next', params=None):
        raise NotImplementedError()



