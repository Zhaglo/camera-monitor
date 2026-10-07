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
        return True
    else:
        return False


if __name__ == '__main__':
    result = set_fps(device, 30)
    if result:
        print('FPS обновлен')
    else:
        print('Некорректный FPS')
    print(result, device['fps'])

    result = set_fps(device, -5)
    if result:
        print('FPS обновлен')
    else:
        print('Некорректный FPS')
    print(result, device['fps'])

    print(f'Камера {device['device_id']}: {device['status']}, {device['resolution']}, {device['fps']} FPS')
