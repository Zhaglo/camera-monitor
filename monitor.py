import logging
import time
import argparse

import asyncio

import httpx


def parse_args():
    parser = argparse.ArgumentParser(description='Мониторинг сетевых камер')
    parser.add_argument('urls', nargs='+', help='Адреса API состояния камер')
    parser.add_argument('--timeout', type=float, default=5, help='Таймаут в секундах')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout должен быть больше нуля')
    return args


async def get_device_state(client, url):
    logging.info('Запрашиваем состояние устройства: %s', url)

    response = await client.get(url)
    response.raise_for_status()
    return response.json()


async def poll_device(client, url):
    try:
        state = await get_device_state(client, url)
        print(state)
    except httpx.HTTPStatusError as error:
        logging.error('Ошибка HTTP: %s устройства %s', error.response.status_code, url)
    except httpx.TimeoutException:
        logging.error('Время ожидания устройства %s превышено', url)
    except httpx.RequestError as error:
        logging.error('Устройство %s недоступно: %s', url, error)


async def main(device_urls, timeout):
    async with httpx.AsyncClient(timeout=timeout, trust_env=False) as client:
        started_at = time.perf_counter()
        await asyncio.gather(
            *(poll_device(client, url) for url in device_urls)
        )
        elapsed = time.perf_counter() - started_at
        print(f'Опрос занял {elapsed:.2f}s')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
    )

    args = parse_args()

    asyncio.run(main(args.urls, args.timeout))
