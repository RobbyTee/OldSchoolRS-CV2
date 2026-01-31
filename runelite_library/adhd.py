from pyautogui import position, press, moveTo
from runelite_library.area import inventory
from runelite_library.filters import coordinate_in_area
from runelite_library.window_management import capture_runelite_window
from time import sleep

import pyautogui
import random
from too_many_items import Interfaces




def adhd():
    decision = int(random.uniform(0,20))
    random_time = random.uniform(0.25, 0.8)
    if decision == 1:
        x,y = position()
        random_int = random.uniform(1, 60)
        x = x + random_int
        y = y + random_int
        moveTo(x, y, duration=random_time, tween=pyautogui.easeInOutQuad)

    elif decision == 2:
        press(Interfaces.stats_icon)
        sleep(1)
        screenshot = capture_runelite_window()
        x,y = coordinate_in_area(bounds=inventory.bounds,
                                          screenshot=screenshot)
        moveTo(x, y, duration=random_time, tween=pyautogui.easeInOutQuad)
        sleep(random.uniform(1, 5))
        press(Interfaces.inventory_icon)
        

    elif decision == 3:
        pass
    elif decision == 4:
        pass
    elif decision == 5:
        pass
    else:
        return