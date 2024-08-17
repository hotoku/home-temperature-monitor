import base64
import hashlib
import hmac
import json
import time
import uuid
from pprint import pprint

import certifi
import urllib3
from pydantic import BaseModel


class SwitchBot(BaseModel):
    token: str
    secret: str
    device_id: str


def load_credentials() -> SwitchBot:
    with open("credentials/switchbot.json") as f:
        return SwitchBot.model_validate_json(f.read())


data = load_credentials()
token = data.token
secret = data.secret
nonce = uuid.uuid4()
t = int(round(time.time() * 1000))
string_to_sign = '{}{}{}'.format(token, t, nonce)

string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(secret, 'utf-8')

sign = base64.b64encode(
    hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

apiHeader = {}
apiHeader['Authorization'] = token
apiHeader['Content-Type'] = 'application/json'
apiHeader['charset'] = 'utf8'
apiHeader['t'] = str(t)
apiHeader['sign'] = str(sign, 'utf-8')
apiHeader['nonce'] = str(nonce)


http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)

host = "https://api.switch-bot.com"
ret = http.request("get", url=host +
                   f"/v1.1/devices/{data.device_id}/status", headers=apiHeader)
val = ret.json()

pprint(val)
