import mss
import numpy as np
import subprocess

from time import sleep


def activate_app(appname):
    name = appname.lower()
    result = subprocess.check_output(['wmctrl','-l']).decode()
    for line in result.splitlines():
        if appname.lower() in line.lower():
            subprocess.run(['wmctrl','-a', name])
            sleep(0.2)
            return True
    return False


def get_active_window_bounds():
    win_id = subprocess.check_output(
        ['xdotool', 'getactivewindow']
    ).decode().strip()

    bounds = subprocess.check_output(
        ['xdotool', 'getwindowgeometry', '--shell', win_id]
    ).decode()

    values = {}
    for line in bounds.splitlines():
        key, val = line.split('=')
        values[key] = int(val)

    x1 = values["X"]
    y1 = values["Y"]
    x2 = x1 + values["WIDTH"]
    y2 = y1 + values["HEIGHT"]

    return x1, y1, x2, y2


def offset_area_to_absolute(relative_area, client_bounds):
    x_offset, y_offset = client_bounds[0], client_bounds[1]
    return [
        relative_area[0] + x_offset,
        relative_area[1] + y_offset,
        relative_area[2] + x_offset,
        relative_area[3] + y_offset
    ]


def capture_runelite_window(name=None):  
    x1, y1, x2, y2 = get_active_window_bounds()
    bounds = {
        "top": y1,
        "left": x1,
        "width": x2 - x1,
        "height": y2 - y1
    }

    with mss.mss() as sct:
        screenshot = sct.grab(bounds)
        img_np = np.array(screenshot)
        if name:
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=name)
        return img_np