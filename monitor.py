import logging
import time

import asyncio

import httpx


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


async def main():
    device_urls = ['http://127.0.0.1:8001/state', 'http://127.0.0.1:8000/state']

    async with httpx.AsyncClient(timeout=5, trust_env=False) as client:
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

    asyncio.run(main())
