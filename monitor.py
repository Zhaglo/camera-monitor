import json
from urllib.request import urlopen


with urlopen('http://127.0.0.1:8000/state', timeout=5) as response:
    body = response.read()
    body = json.loads(body)
    print(f"{body['device_id']} {body['status']}, {body['fps']}")