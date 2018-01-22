import os
import platform
import pytest
from donkeycar.parts.datastore import Tub
from donkeycar.parts.simulation import SquareBoxCamera, MovingSquareTelemetry


def on_pi():
    if 'arm' in platform.machine():
        return True
    return False

temp_tub_path = None

@pytest.fixture
def tub_path(tmpdir):
    tub_path = tmpdir.mkdir('tubs').join('tub')
    return str(tub_path)


@pytest.fixture
def tub(tub_path):
    t = create_sample_tub(tub_path, records=128)
    return t

def create_sample_tub(path, records=128):
    inputs=['cam/image_array', 'user/angle', 'user/throttle']
    types=['image_array', 'float', 'float']
    t = Tub(path, inputs=inputs, types=types)
    cam = SquareBoxCamera()
    tel = MovingSquareTelemetry()
    for _ in range(records):
        x, y = tel.run()
        img_arr = cam.run(x, y)
        t.put_record({'cam/image_array': img_arr, 'user/angle': x, 'user/throttle':y})

    global temp_tub_path
    temp_tub_path = t
    print("setting temp tub path to:", temp_tub_path)

    return t




