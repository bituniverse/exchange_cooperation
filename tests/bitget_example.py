# coding=utf-8

from exchanges.bitget_swap import bitgetswap

bitgetswap.apiKey ="bg_bbe24d57657d45de54210905888024e2"
bitgetswap.secret ="61629c51d4b5f127ace628fba9feb41a3272fee468d28deea35a23e121b37188"
bitgetswap.password ="11111111"
b=bitgetswap()


print(bitgetswap.fetch_time(b, {}))

#print(bitgetswap.fetch_markets(b,{}))

#print(bitgetswap.fetch_markets_by_type(b,"swap",{}))

#print(bitgetswap.fetch_ticker(b,"CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_order(b,"623755167610699713","CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_tickers(b,"CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_accounts(b,{}))

#print(bitgetswap.fetch_balance(b,{}))

#print(bitgetswap.fetch_currencies(b,{}))

#print(bitgetswap.fetch_closed_orders(b,"CMT_BTCUSDT",1598759333933,None,{}))

#print(bitgetswap.fetch_deposits(b,"BTC",None,None,{}))   //币币的

#print(bitgetswap.fetch_withdrawals(b,"BTC",None,None,{})) //币币的

#print(bitgetswap.fetch_trades(b,"CMT_BTCUSDT",100,1598759333933,{}))

#print(bitgetswap.create_order(b,"CMT_BTCUSDT","limit","buy",100.23,None,{}))

#print(bitgetswap.cancel_order(b,"623755167610699713","CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_open_orders(b,"CMT_BTCUSDT",None,None,{}))

#print(bitgetswap.fetch_order_trades(b,"623755167610699713","CMT_BTCUSDT",1598759333933,100,{}))

#print(bitgetswap.fetch_tickers_by_type(b,"swap","CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_ohlcv(b,"CMT_BTCUSDT","1m",1598759333933,100,{}))

#print(bitgetswap.fetch_order_book(b,"CMT_BTCUSDT",100,{}))
















