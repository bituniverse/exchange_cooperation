class SpotApi:


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
       fetch_currencies
    """

    def fetch_currencies(self, params={}):

        raise NotImplementedError()

    """
       fetch_order_book
    """
    def fetch_order_book(self, symbol, params={}):

        raise NotImplementedError()

    """
       fetch_ticker
    """
    def fetch_ticker(self, symbol,params={}):

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
      fetch_accounts
    """
    def fetch_accounts(self, params={}):

        raise NotImplementedError()

    """
      fetch_balacne
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
       fetch_deposits
    """
    def fetch_deposits(self, code=None, since=None, limit=None, params={}):

        raise NotImplementedError()


    """
      fetch_order_trades
    """
    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):

        raise NotImplementedError()

    """
     fetch_my_trades
    """
    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):

        raise NotImplementedError()







