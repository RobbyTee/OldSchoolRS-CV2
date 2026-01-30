from config import STAFF, HIGH_ALCHEMY
from enum import Enum, auto
from pyautogui import press, moveTo
from runelite_library.area import play_area, inventory, whole
from runelite_library.bank import open_bank
from runelite_library.check_charges import log_use
from runelite_library.filters import find_by_template, find_by_templates, wait
from runelite_library.interaction import click, right_click, use_rgb1_on_rgb2
from runelite_library.logger import log_event, log_state, read_prev_state
from runelite_library.window_management import capture_runelite_window
from time import sleep
from too_many_items import Pathing, Bank, Items, Menu, Objects, Misc

def withdraw_skills_necklace():
    """
    With the bank open, this will withdraw 1 skills necklace
    from the tab "ALL".
    """
    to_withdraw_necklace = [
        Bank.quantity_1, Bank.tab_all, Items.skills_necklace
    ]

    for template in to_withdraw_necklace:
        if not click(wait(template=template, timeout=5)):
            log_event(f"Could not find {template}")
            return False
    
    return True


def farming_guild_teleport():
    """
    Uses the skills necklace to teleport to the farming guild
    """
    if not right_click(wait(template=Items.skills_necklace)):
        return False

    if not click(wait(template=Menu.rub)):
        return False
    
    sleep(1)

    press('6')
    
    sleep(3)
    
    return True
