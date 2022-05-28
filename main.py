from dextrade import Dextrade, PrivateCommands, PublicCommands, OrderReqType, OrderReqTypeTrade
from dotenv import load_dotenv
import os
import json
from pprint import pprint
import random

load_dotenv()

key = os.environ.get("KEY")
secret = os.environ.get("SECRET")

d = Dextrade(key=key, secret=secret)



# Test private commands
a = d(PrivateCommands.ACTIVEORDERS_, args={})
print(a.status_code)
print(a.text)

balance = {"USDT":0, "CYRUS":0}
b = d(PrivateCommands.BALANCES_, args={})
b = b.json()["data"]["list"]
print("Available balances: ")
for i,_ in enumerate(b):
    if _["currency"]["iso3"] == "USDT":
        balance["USDT"] = _["balance_available"]*1E-8
    if _["currency"]["iso3"] == "CYRUS":
        print(_)
        balance["CYRUS"] = _["balance_available"]*1E-8
# get available balance
print(balance)

print("Sending order in progress...")
args = {
    "type_trade": OrderReqTypeTrade.LIMIT.value,
    "type": OrderReqType.BUY.value,
    "rate": 1.45361540,
    "stop_rate": 0,
    "volume": round(random.uniform(0.3*balance["USDT"], 0.7*balance["USDT"]),2),
    "pair": "CYRUSUSDT"
}
a = d(PrivateCommands.CREATEORDER_, args=args)
print(a.status_code)
print(a.text)
a = a.json()


# Test public commands
# a = d(PublicCommands.SYMBOLS_)
# a = a.content.decode("utf-8")
# a = json.loads(a)
# a = list(map(lambda _: _["pair"], a['data']))

# pair = "CYRUSUSDT" # id:8941
# a = d(PublicCommands.ORDERBOOK_, args={'pair': pair}).content.decode("utf-8")
# a = json.loads(a)
