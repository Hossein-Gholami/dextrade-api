from enum import Enum
from flask import session
# import requests
from requests.exceptions import RequestException
from requests import Session
# from urllib.parse import urlencode
from hmac import new
from hashlib import sha256
import hashlib
import json
from time import time
from pprint import pprint

class PublicCommands(Enum):
    SYMBOLS_ = "symbols"
    TICKER_ = "ticker"
    ORDERBOOK_ = "orderbook"
    TRADEHIST_ = "trade_hist"

class PrivateCommands(Enum):
    CREATEORDER_ = "create_order"
    ACTIVEORDERS_ = "active_orders"
    GETORDER_ = "get_order"
    DELORDER_ = "del_order"
    ORDERHIST_ = "order_hist"
    BALANCES_ = "balance"

class OrderReqTypeTrade(Enum):
    LIMIT = 0
    MARKET = 1
    STOPLIMIT = 2
    QUICKMARKET = 3

class OrderReqType(Enum):
    BUY = 0
    SELL = 1


class DextradeError(Exception):
    """ Exception for handling dextrader api errors """
    pass

class RetryException(DextradeError):
    """ Exception for retry decorator """
    pass

dextrade_api = "https://api.dex-trade.com/v1"

endpoints = {
    # public endpoints
    PublicCommands.SYMBOLS_.value: r'/public/symbols',
    PublicCommands.TICKER_.value: r'/public/ticker?pair=%s',
    PublicCommands.ORDERBOOK_.value: r'/public/book?pair=%s',
    PublicCommands.TRADEHIST_.value: r'/public/trades?pair=%s',
    # private endpoints
    PrivateCommands.CREATEORDER_.value: r'/private/create-order',
    PrivateCommands.ACTIVEORDERS_.value: r'/private/orders',
    PrivateCommands.GETORDER_.value: r'/private/get-order',
    PrivateCommands.DELORDER_.value: r'/private/delete-order',
    PrivateCommands.ORDERHIST_.value: r'/private/history',
    PrivateCommands.BALANCES_.value: r'/private/balances',
}

class Dextrade(object):
    def __init__(self, key=False, secret=False) -> None:
        self.session = Session()
        self.key = key
        self.secret = secret

    def __call__(self, command: Enum, args: dict):
        assert isinstance(command, Enum)
        assert (command in PublicCommands or command in PrivateCommands)

        if command in PublicCommands:
            payload = {}
            if command == PublicCommands.SYMBOLS_:
                payload['url'] = dextrade_api+endpoints[command.value]
                # response = requests.get(dextrade_api+endpoints[command.value])
                # return response
            else:
                assert 'pair' in args, "for this command 'pair' should be provided"
                payload['url'] = dextrade_api+endpoints[command.value]%args['pair']
                # response = requests.get(dextrade_api+endpoints[command.value]%args['pair'])
                # return response
            self.session.get(**payload)

        if command in PrivateCommands:
            req_id = f"{time()}".replace(".", "")
            payload = {}
            payload['url'] = dextrade_api+endpoints[command.value]
            args['request_id'] = req_id
            payload['data'] = json.dumps(args)

            def prep_msg(args:dict) -> str:
                assert isinstance(args, dict)
                s = sorted(args.items(), key=lambda t: t[0])
                # print(urlencode(s))
                s = "".join(list(map(lambda i: str(i[1]), s)))
                s += ""+self.secret
                # print(s)
                return s

            # sign = new(
            #     self.secret.encode('utf-8'),
            #     # urlencode(args).encode('utf-8'),
            #     prep_msg(args).encode("utf-8"),
            #     sha256
            # ).hexdigest()
            sign = hashlib.sha256(prep_msg(args).encode("utf-8")).hexdigest()
            # print(f"key: {self.key}, \nsecret: {self.secret}")
            # print(f"data: {payload['data']}")
            print(f"signature: {prep_msg(args)}")
            payload['headers'] = {
                'Content-Type': 'application/json',
                'Login-Token': self.key,
                'X-Auth-Sign': sign
            }
            print("payload: ", end="")
            pprint(payload)
            ret = self.session.post(**payload)
            return ret
            # return self.handle_returned(ret)
    
    def handle_returned(self, data):
        pass