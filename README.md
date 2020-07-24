
# Exchange APIs of BitUniverse

BitUniverse Trading Bot's integration with Exchange APIs. 

This project bases on [CCXT](https://github.com/ccxt/ccxt)


## What is CCXT?
> A JavaScript / Python / PHP library for cryptocurrency trading and e-commerce with support for many bitcoin/ether/altcoin exchange markets and merchant APIs.

## What's the difference between CCXT and this

In BitUniverse, we integrate Exchanges with CCXT.

CCXT is a full-featured library for cryptocurrency trading.
However, for building a trading bot, we only need part of its features, while some other useful APIs or parameters are not unified by CCXT.
So we made our own definition of Exchange APIs for our trading bots usage.

All the API definitions are based on CCXT's definitions. So it's easy to reuse CCXT as the implementation.

However, CCXT is not necessary for the implementation. 
We only made the definition. People could implement the APIs with any libraries they want and just satisfy the definition.

If the Exchange has been supported by CCXT, the CCXT' implementation could be used as the BU's implementation directly.
If the Exchange is not supported by CCXT, we highly recommend to implement the APIs with CCXT. 

CCXT supports JavaScript, Python and PHP, while in BitUniverse, we only need the Python implementation. 
You can either implement the APIs in CCXT with JavaScript and use its instrument to convert it into Python and PHP, or just implement the Python version.

## Future support

While CCXT supports future trading as well. 
But their implementation was based on spot trading, which losses a lot of features and information for futures.

So if the future trading needs to be supported, the CCXT's implementation cannot be used directly. 

## Requirements

1. Python3.8 or higher
2. All the implementation should support async calling with "asyncio" lib in Python. If you are using CCXT, use "ccxt.async_support" package

## How to integrate an exchange to BitUniverse

1. Make your own fork of this repository 
2. Create the .py file in "exchanges" folder with the name of the exchange and market, eg. binance_swap.py
3. Implement the APIs defined in "spot_api.py" for Spot trading or "swap_api.py" for Perpetual contract trading.
4. Make sure your implementation passes all the unit test cases
5. Create a pull request to this repository

## Limitations

1. We only support Spot and Perpetual futures for Now.
   And for Perpetual futures, only fiat based futures are supported. 
   Coin based futures are still in development.
   
2. For Perpetual futures, we highly recommend to support isolate margin mode. 
   If not, the trading bots will loss the abilities of monitoring and controlling the risk.
   And users have to take care of the force liquidation price by themselves.   

3. CCXT uses "float" type to handle number fields. However float type [may loss the precision](https://docs.python.org/3/tutorial/floatingpoint.html).
   We highly recommend to use decimal package in the implementation. 
   Considering of python's "json" library will convert numbers to float by default, we recommend to use "[simplejson](https://simplejson.readthedocs.io/en/latest/)" instead of it.
   Just replace `json.loads(some_json_string)` with `simplejson.loads(some_json_string, use_decimal=True)`
   Or you can also inherit ccxt_ext to solve this. Besides, transfer numbers as string is also supported.
   
   See [example](blob/master/examples/binance_swap.py) for more details

4. Since BitUniverse has extremely strict safety structure. We will hook the signature generation codes to our safety system. 
   We will not pass users' APIKey and APISecret into the API object as CCXT dose. 
   So make sure **NOT** to cache any user specific data into the API instance.
   If necessary, client of the API should take the responsibility to hold it and pass it to API through parameters.
   "params" for each API could be used for this.

## Reference

* https://github.com/ccxt/ccxt/wiki
