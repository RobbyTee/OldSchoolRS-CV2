from runelite_library.area import minimap, whole
from runelite_library.window_management import activate_app, get_active_window_bounds
from runelite_library.interaction import click, right_click
from runelite_library.bank import open_bank
from too_many_items import Bank, Login, Normal_Spellbook
from runelite_library.login import login
from runelite_library.interaction import find_by_template,find_by_color
from runelite_library.filters import wait
from time import sleep

import mss
import numpy as np
import subprocess


activate_app("runelite")

right_click(wait(template=Normal_Spellbook.house_tele))

