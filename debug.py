from pyautogui import press
from runelite_library.window_management import activate_app, capture_runelite_window
from runelite_library.login import login
from runelite_library.logger import read_prev_state
from runelite_library.check_charges import log_use, check_charges
from tasks.fungus import Fungus
from tasks.master_farmer import Pickpocket
from tasks.mahogany_logs import ChopMahoganyTrees, MahoganyStates
from runelite_library.interaction import click, get_worn_equipment
from too_many_items import Bank, Items, Menu
from runelite_library.area import (whole, bank_window, 
                                   minimap, play_area, inventory)
from runelite_library.filters import (find_by_template, coordinate_in_area, 
                            wait, find_by_color, find_all_by_color, area_by_color,
                            find_by_cic)
from time import sleep
from too_many_items import Pathing
from tasks.battlestaffs import MakeStaffs
import random

activate_app('runelite')

completed_staff = (155, 236, 228)
orb = (34, 144, 133)
battlestaff = (30, 130, 70)
nature_runes = (135, 255, 135)

m = MakeStaffs()
m.start()