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

    device_urls = ['http://127.0.0.1:8001/state', 'http://127.0.0.1:8000/state']

    for url in device_urls:
        try:
            state = get_device_state(url=url)
            print(state)
        except HTTPError as error:
            logging.error('Ошибка HTTP: %s устройства %s', error.code, url)
        except URLError as error:
            logging.error('Устройство %s недоступно: %s', url, error.reason)
        except TimeoutError:
            logging.error('Время ожидания устройства %s превышено', url)
