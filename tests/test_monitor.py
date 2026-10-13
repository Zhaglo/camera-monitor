import asyncio

import httpx

from monitor import poll_device


def test_poll_device_success():
    def handler(request):
        return httpx.Response(
            200,
            json={'device_id': 'test-camera', 'fps': 25},
        )

    async def run_check():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            return await poll_device(client, 'http://camera/state')

    result = asyncio.run(run_check())

    assert result['success'] is True
    assert result['url'] == 'http://camera/state'
    assert result['state'] == {
        'device_id': 'test-camera',
        'fps': 25
    }


def test_poll_device_http_error():
    def handler(request):
        return httpx.Response(503)

    async def run_check():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            return await poll_device(client, 'http://camera/state')

    result = asyncio.run(run_check())

    assert result['success'] is False
    assert result['error_type'] == 'http'
    assert result['status_code'] == 503


def test_poll_device_timeout():
    def handler(request):
        raise httpx.ReadTimeout('Имитация таймаута', request=request)

    transport = httpx.MockTransport(handler)

    async def run_check():
        async with httpx.AsyncClient(transport=transport) as client:
            return await poll_device(client, 'http://camera/state')

    result = asyncio.run(run_check())

    assert result['success'] is False
    assert result['error_type'] == 'timeout'
