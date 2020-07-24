from decimal import Decimal
import simplejson
from ccxt.async_support import Exchange
import collections


class CCXTExtension:
    @staticmethod
    def extend(*args):
        if args is not None:
            result = None
            if type(args[0]) is collections.OrderedDict:
                result = collections.OrderedDict()
            else:
                result = {}
            for arg in args:
                if not arg:
                    continue
                result.update(arg)
            return result
        return {}

    @staticmethod
    def safe_decimal(dictionary, key, default_value=None):
        value = default_value
        try:
            if Exchange.key_exists(dictionary, key):
                value = Decimal(str(dictionary[key]))
        except ValueError as e:
            value = default_value
        return value

    @staticmethod
    def safe_decimal_2(dictionary, key1, key2, default_value=None):
        return Exchange.safe_either(CCXTExtension.safe_decimal, dictionary, key1, key2, default_value)

    def parse_json(self, http_response):
        try:
            if Exchange.is_json_encoded_object(http_response):
                return simplejson.loads(http_response, use_decimal=True)
        except ValueError:  # superclass of JsonDecodeError (python2)
            pass

    @staticmethod
    def unjson(input):
        return simplejson.loads(input, use_decimal=True)

    @staticmethod
    def json(data, params=None):
        return simplejson.dumps(data, separators=(',', ':'))