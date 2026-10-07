from fastapi import FastAPI
from device import device

app = FastAPI()


@app.get('/state')
def get_state():
    return device
