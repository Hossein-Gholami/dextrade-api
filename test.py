from dotenv import load_dotenv
import requests
from hmac import new
from hashlib import sha256
# from urllib.parse import urlencode
from time import time
import os
import json
# from binascii import unhexlify

load_dotenv()

key, secret = os.environ.get('KEY'), os.environ.get('SECRET')

data = {"request_id":f"{time()}".replace(".","")}

payload = {}
payload["url"] = "https://api.dex-trade.com/v1/private/orders"
payload["data"] = json.dumps(data)

# sign = new(secret.encode('utf-8'), f"{data['request_id']}".encode('utf-8'), sha256)
sign = new(secret.encode('utf-8'), data["request_id"].encode('utf-8'), sha256)
# sign = new(unhexlify(key), unhexlify(f"{data}"), sha256)

payload["headers"] = {
    'content-type': 'application/json',
    'login-token': key,
    'x-auth-sign': sign.hexdigest()
}

from pprint import pprint
pprint(payload)

r = requests.post(**payload)
# r = requests.post(url=payload['url'], json=f"{payload['data']}", headers=payload['headers'])
print(r.status_code)
print(r.text)
