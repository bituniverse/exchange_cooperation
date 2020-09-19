# coding=utf-8

from exchanges.bitget_swap import bitgetswap

bitgetswap.apiKey ="bg_b6bf2c1e88e352f6d03a0d02544f1354"
bitgetswap.secret ="8ecba60d41f18be31a35371800a22628b5d9a8ec5f4b9a084d862f85770306f1"
bitgetswap.password ="11111111"
b=bitgetswap()



#print(bitgetswap.fetch_orders(b,"CMT_BTCUSDT",None,None,None,"",{"from":"1","to":"1","limit":"100","status":"5"}))

#print(bitgetswap.fetch_positions(b))

#print(bitgetswap.change_leverage(b,"CMT_BTCUSDT",10,None,{"holdSide":2}))

#print(bitgetswap.change_margin_type(b,"CMT_BTCUSDT",None,None,{"holdModel":1}))

#print(bitgetswap.fetch_position_side(b,"CMT_BTCUSDT"))

#print(bitgetswap.fetch_funding_records(b,"CMT_BTCUSDT",None,None,None,None,{"pageIndex":1,"pageSize":50}))

#print(bitgetswap.change_isolated_margin(b,"CMT_BTCUSDT",None,None,10,{"positionType":1,"type":1}))

#print(bitgetswap.fetch_incomes(b,"CMT_BTCUSDT",None,None,None,None,{"pageIndex":1,"pageSize":50,"createDate":70}))

#print(bitgetswap.fetch_trading_fee_rates(b))



#print(bitgetswap.fetch_time(b, {}))

#print(bitgetswap.fetch_markets(b,{}))

#print(bitgetswap.fetch_markets_by_type(b,"swap",{}))

#print(bitgetswap.fetch_ticker(b,"CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_order(b,"623755167610699713","CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_tickers(b,"CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_accounts(b,{}))

#print(bitgetswap.fetch_balance(b,{}))

#print(bitgetswap.fetch_currencies(b,{}))

#print(bitgetswap.fetch_closed_orders(b,"CMT_BTCUSDT",1598759333933,None,{}))

#print(bitgetswap.fetch_deposits(b,"BTC",None,None,{}))

#print(bitgetswap.fetch_withdrawals(b,"BTC",None,None,{}))

#print(bitgetswap.fetch_trades(b,"CMT_BTCUSDT",100,1598759333933,{}))

#print(bitgetswap.create_order(b,"CMT_BTCUSDT","limit","buy",100.23,None,{}))

#print(bitgetswap.cancel_order(b,"623755167610699713","CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_open_orders(b,"CMT_BTCUSDT",None,None,{}))

#print(bitgetswap.fetch_order_trades(b,"623755167610699713","CMT_BTCUSDT",1598759333933,100,{}))

#print(bitgetswap.fetch_tickers_by_type(b,"swap","CMT_BTCUSDT",{}))

#print(bitgetswap.fetch_ohlcv(b,"CMT_BTCUSDT","1m",1598759333933,100,{}))

#print(bitgetswap.fetch_order_book(b,"CMT_BTCUSDT",100,{}))
















