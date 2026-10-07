import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def get_device_state(url, timeout=5):
    with urlopen(url, timeout=timeout) as response:
        body = response.read()
        return json.loads(body)


if __name__ == '__main__':
    try:
        state = get_device_state(url='http://127.0.0.1:8000/state')
        print(state)
    except HTTPError as error:
        print(f'Ошибка HTTP: {error.code}')
    except URLError as error:
        print(f'Устройство недоступно: {error.reason}')
    except TimeoutError:
        print('Время ожидания превышено')
