device = {
    'device_id': 'entrance-01',
    'name': 'camera',
    'status': 'online',
    'resolution': '1920x1080',
    'fps': 25
}


def set_offline(device):
    device['status'] = 'offline'


def set_online(device):
    device['status'] = 'online'


set_offline(device)
set_online(device)

print(f'Камера {device['device_id']}: {device['status']}, {device['resolution']}, {device['fps']} FPS')
