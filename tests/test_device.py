from device import set_fps


def test_set_fps_rejects_negative_value():
    device = {'fps': 25}

    result = set_fps(device, -5)

    assert result is False
    assert device['fps'] == 25


def test_set_fps_accepts_positive_value():
    device = {'fps': 25}

    result = set_fps(device, 30)

    assert result is True
    assert device['fps'] == 30


def test_set_fps_rejects_zero():
    device = {'fps': 25}

    result = set_fps(device, 0)

    assert result is False
    assert device['fps'] == 25
