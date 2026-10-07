import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


try:
    with urlopen('http://127.0.0.1:8000/state', timeout=5) as response:
        body = response.read()
        body = json.loads(body)
        print(f"{body['device_id']} {body['status']}, {body['fps']}")
except HTTPError as error:
    print(f'Ошибка HTTP: {error.code}')
except URLError as error:
    print(f'Устройство недоступно: {error.reason}')
