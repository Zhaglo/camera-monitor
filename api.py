from fastapi import FastAPI

from pydantic import BaseModel, Field

from device import device, set_fps

app = FastAPI()


class DeviceSettings(BaseModel):
    fps: int = Field(gt=0)


@app.get('/state')
def get_state():
    return device


@app.patch('/settings')
def update_settings(settings: DeviceSettings):
    set_fps(device, settings.fps)
    return device
