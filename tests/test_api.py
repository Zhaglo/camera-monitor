from fastapi.testclient import TestClient

from api import app
from device import device


def test_settings_rejects_zero_fps():
    with TestClient(app) as client:
        previous_fps = device['fps']

        response = client.patch('/settings', json={'fps': 0})

        assert response.status_code == 422
        assert device['fps'] == previous_fps


def test_settings_updates_fps():
    previous_fps = device['fps']

    try:
        with TestClient(app) as client:
            response = client.patch('/settings', json={'fps': 30})

            assert response.status_code == 200
            assert response.json()['fps'] == 30
            assert device['fps'] == 30
    finally:
        device['fps'] = previous_fps
