from pyautogui import moveTo
from runelite_library.area import minimap, whole

from runelite_library.window_management import (
    activate_app, get_active_window_bounds, capture_runelite_window
)
from runelite_library.interaction import click, right_click
from runelite_library.bank import open_bank
from too_many_items import Bank, Login, Normal_Spellbook, Items
from runelite_library.login import login
from runelite_library.interaction import find_by_template,find_by_color
from runelite_library.filters import wait, find_all_by_template
from time import sleep
from tasks.tree_run import TreeRun
import mss
import numpy as np
import subprocess


activate_app("runelite")

#t = TreeRun()
#t.start()

screenshot = capture_runelite_window()
coords = find_all_by_template(screenshot=screenshot, template_path=Items.sapling)
print(f"Found {len(coords)} saplings.")
#for coord in coords:
#    moveTo(coord)
#    sleep(2)