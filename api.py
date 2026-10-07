import os
import time

from fastapi import FastAPI

from pydantic import BaseModel, Field

from device import device, set_fps

response_delay = float(os.getenv('DEVICE_DELAY', '0'))
if response_delay < 0:
    raise ValueError('DEVICE_DELAY должен быть неотрицательным')

app = FastAPI()


class DeviceSettings(BaseModel):
    fps: int = Field(gt=0)


@app.get('/state')
def get_state():
    time.sleep(response_delay)
    return device


@app.patch('/settings')
def update_settings(settings: DeviceSettings):
    set_fps(device, settings.fps)
    return device
