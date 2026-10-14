import logging
import time
import argparse
import json

import asyncio

import httpx


def parse_args():
    parser = argparse.ArgumentParser(description='Мониторинг сетевых камер')
    parser.add_argument('urls', nargs='+', help='Адреса API состояния камер')
    parser.add_argument('--timeout', type=float, default=5, help='Таймаут в секундах')
    parser.add_argument('--output', help='Путь к JSON-отчету')
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
        return {
            'url': url,
            'success': True,
            'state': state,
        }
    except httpx.HTTPStatusError as error:
        logging.error('Ошибка HTTP: %s устройства %s', error.response.status_code, url)
        return {
            'url': url,
            'success': False,
            'error_type': 'http',
            'error': str(error),
            'status_code': error.response.status_code,
        }
    except httpx.TimeoutException:
        logging.error('Время ожидания устройства %s превышено', url)
        return {
            'url': url,
            'success': False,
            'error_type': 'timeout',
            'error': 'Время ожидания превышено',
        }
    except httpx.RequestError as error:
        logging.error('Устройство %s недоступно: %s', url, error)
        return {
            'url': url,
            'success': False,
            'error_type': 'network',
            'error': str(error),
        }
    except json.JSONDecodeError as error:
        logging.error('Устройство %s вернуло некорректный JSON: %s', url, error)
        return {
            'url': url,
            'success': False,
            'error_type': 'invalid_json',
            'error': str(error),
        }


async def main(device_urls, timeout, output):
    async with httpx.AsyncClient(timeout=timeout, trust_env=False) as client:
        started_at = time.perf_counter()
        results = await asyncio.gather(
            *(poll_device(client, url) for url in device_urls)
        )
        elapsed = time.perf_counter() - started_at
        report = {
            'elapsed_seconds': elapsed,
            'results': results,
        }

        if output:
            with open(output, 'w', encoding='utf-8') as file:
                json.dump(report, file, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
    )

    args = parse_args()

    asyncio.run(main(args.urls, args.timeout, args.output))
