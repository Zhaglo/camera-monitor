import json
import logging
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def get_device_state(url, timeout=5):
    logging.info('Запрашиваем состояние устройства: %s', url)

    with urlopen(url, timeout=timeout) as response:
        body = response.read()
        return json.loads(body)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
    )

    try:
        state = get_device_state(url='http://127.0.0.1:8000/state')
        print(state)
    except HTTPError as error:
        logging.error('Ошибка HTTP: %s', error.code)
    except URLError as error:
        logging.error('Устройство недоступно: %s', error.reason)
    except TimeoutError:
        logging.error('Время ожидания превышено')
