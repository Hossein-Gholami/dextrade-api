from dextrade import Dextrade, PrivateCommands, PublicCommands, OrderReqType, OrderReqTypeTrade
from dotenv import load_dotenv
import os
import json
from pprint import pprint

load_dotenv()

key = os.environ.get("KEY")
secret = os.environ.get("SECRET")

d = Dextrade(key=key, secret=secret)



# Test private commands
a = d(PrivateCommands.ACTIVEORDERS_, args={})

# args = {
#     "type_trade": OrderReqTypeTrade.LIMIT.value,
#     "type": OrderReqType.BUY.value,
#     "rate": 1.1,
#     "stop_rate": 0,
#     "volume": 10,
#     "pair": "CYRUSUSDT"
# }
# a = d(PrivateCommands.CREATEORDER_, args=args)

print(a.status_code)
print(a.text)

# Test public commands
# a = d(PublicCommands.SYMBOLS_)
# a = a.content.decode("utf-8")
# a = json.loads(a)
# a = list(map(lambda _: _["pair"], a['data']))

# pair = "CYRUSUSDT" # id:8941
# a = d(PublicCommands.ORDERBOOK_, args={'pair': pair}).content.decode("utf-8")
# a = json.loads(a)
