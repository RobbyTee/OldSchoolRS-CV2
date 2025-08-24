from config import (
    SUPER_ENERGY
)

from enum import Enum, auto
from pyautogui import press, moveTo
from runelite_library.area import whole, inventory, play_area
from runelite_library.filters import find_by_template, wait, find_by_templates
from runelite_library.interaction import click, right_click
from runelite_library.logger import log_state, log_event
from runelite_library.window_management import capture_runelite_window
from runelite_library.bank import open_bank
from time import sleep
from too_many_items import Bank, Items, Misc

def withdraw_if_in_stock(screenshot, item):
    """
    Input screenshot and template path of item. It'll hover over it and check
    if "GOOD" pops up. Used mostly with the bank.
    """
    item_to_withdraw = find_by_template(screenshot, item)

    if item_to_withdraw:
        moveTo(item_to_withdraw)
    else:
        log_event(f"No {str(item)} in stock!", level="error")
        return False

    enough_in_stock = wait(template=Misc.good, bounds=play_area.bounds, timeout=1)

    if enough_in_stock:
        right_click(item_to_withdraw)
        click(wait(template=Bank.withdraw_14))
        return True
    else:
        log_event(f"Not enough {str(item)} in stock.", level="error")
        return False


class PotionState(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    CHOOSE_POTION = auto()
    WITHDRAW_INGREDIENTS = auto()
    COMBINE_INGREDIENTS = auto()
    MAKE_SUPER_ENERGY = auto()
    SUCCESS = auto()
    FAILED = auto()


class MakePotion:
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)
    
    
    def start(self):
        self.state = PotionState.INIT

        while True:
            if self.state == PotionState.INIT:
                self.transition_state(PotionState.OPEN_BANK)
                continue

            elif self.state == PotionState.OPEN_BANK:
                if not open_bank():
                    self.transition_state(PotionState.FAILED)
                    continue

                if not click(wait(template=Bank.tab_ii, timeout=1)):
                    self.transition_state(PotionState.FAILED)
                    continue
                
                if not click(wait(template=Bank.deposit_inventory, timeout=1)):
                    self.transition_state(PotionState.FAILED)
                    continue
                
                screenshot_of_tab_ii = capture_runelite_window()
                self.transition_state(PotionState.CHOOSE_POTION)
            
            elif self.state == PotionState.CHOOSE_POTION:
                if SUPER_ENERGY:
                    unfinished_potion = Items.avantoe_potion_unf
                    secondary_item = Items.mort_myre_fungus
                    self.transition_state(PotionState.WITHDRAW_INGREDIENTS)
                    continue
                else:
                    self.transition_state(PotionState.FAILED)
                    continue
                    
            elif self.state == PotionState.WITHDRAW_INGREDIENTS:
                if not withdraw_if_in_stock(screenshot_of_tab_ii, unfinished_potion):
                    self.transition_state(PotionState.FAILED)
                    continue
                
                if not withdraw_if_in_stock(screenshot_of_tab_ii, secondary_item):
                    self.transition_state(PotionState.FAILED)
                    continue
                
                press('esc')
                self.transition_state(PotionState.COMBINE_INGREDIENTS)
                continue
            
            elif self.state == PotionState.COMBINE_INGREDIENTS:
                click(wait(template=unfinished_potion, timeout=1))
                click(wait(template=secondary_item, timeout=1))
                sleep(1)
                press('space')
                sleep(18)
                self.transition_state(PotionState.SUCCESS)
                continue

            elif self.state == PotionState.SUCCESS:
                return True
            
            elif self.state == PotionState.FAILED:
                return False
