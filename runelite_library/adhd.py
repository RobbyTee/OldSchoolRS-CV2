import pyautogui
import random
import too_many_items as tmi

from environment import find_by_template
from interaction import click
from runelite_library.environment import inventory_area, minimap_area, play_area
from time import sleep


def adhd():
    decision = int(random.uniform(0,20))
    if decision == 1:
        bounds = inventory_area()
        click(find_by_template(tmi.Interfaces.stats_icon, bounds=bounds))
        sleep(3)
        click(find_by_template(tmi.Interfaces.inventory_icon, bounds=bounds))

    elif decision == 2:
        random_x = int(random.uniform(53, 800))
        random_y = int(random.uniform(53, 800))
        random_sleep = int(random.uniform(0, 28))
        print(f'ADHD moment. Sleeping for {random_sleep} seconds.')
        pyautogui.moveTo(random_x, random_y)
        sleep(random_sleep)

    elif decision == 3:
        pass
    elif decision == 4:
        pass
    elif decision == 5:
        pass
    else:
        return