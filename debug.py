from runelite_library.area import minimap, whole
from runelite_library.window_management import activate_app, get_active_window_bounds
from runelite_library.interaction import click
from runelite_library.bank import open_bank
from too_many_items import Bank, Login
from runelite_library.login import login
from runelite_library.interaction import find_by_template,find_by_color
from runelite_library.filters import wait
from time import sleep

import mss
import numpy as np
import subprocess

def capture_runelite_window(name=None):  
    x1, y1, x2, y2 = get_active_window_bounds()
    print(get_active_window_bounds())
    bounds = {
        "top": y2 - 280,
        "left": x2 - 230,
        "width": 15,
        "height": 15
    }
    example = {
        "top": y1 + 15,
        "left": x2 - 200,
        "width": 20,
        "height": 20
    }
    with mss.mss() as sct:
        screenshot = sct.grab(bounds)
        img_np = np.array(screenshot)
        if name:
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=name)
        return img_np


activate_app("runelite")
sleep(0.1)

capture_runelite_window("open_test.png")

