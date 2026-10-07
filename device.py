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


def set_fps(device, fps):
    if fps > 0:
        device['fps'] = fps
    else:
        print('FPS должен быть больше нуля')


set_fps(device, 15)
print(device['fps'])
set_fps(device, -5)
print(device['fps'])

print(f'Камера {device['device_id']}: {device['status']}, {device['resolution']}, {device['fps']} FPS')
