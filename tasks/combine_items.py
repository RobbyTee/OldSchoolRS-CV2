from config import (
    SUPER_ENERGY,
    STAMINA,
    GLASS_ORB,
    CRUSH_BIRDNESTS
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

def withdraw_if_in_stock(screenshot, item, quantity):
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
        if quantity == 14:
            click(wait(template=Bank.withdraw_14))
        elif quantity == "all":
            click(wait(template=Bank.withdraw_all))
        return True
    else:
        log_event(f"Not enough {str(item)} in stock.", level="error")
        return False


class ItemState(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    CHOOSE_RECIPE = auto()
    WITHDRAW_INGREDIENTS = auto()
    COMBINE_INGREDIENTS = auto()
    MAKE_SUPER_ENERGY = auto()
    SUCCESS = auto()
    FAILED = auto()


class CombineItems:
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)
    
    
    def start(self):
        self.state = ItemState.INIT

        while True:
            if self.state == ItemState.INIT:
                self.transition_state(ItemState.OPEN_BANK)
                continue

            elif self.state == ItemState.OPEN_BANK:
                if not open_bank():
                    self.transition_state(ItemState.FAILED)
                    continue

                if not click(wait(template=Bank.tab_ii, timeout=1)):
                    self.transition_state(ItemState.FAILED)
                    continue
                
                if not click(wait(template=Bank.deposit_inventory, timeout=1)):
                    self.transition_state(ItemState.FAILED)
                    continue
                
                sleep(1.5)
                screenshot_of_tab_ii = capture_runelite_window()
                self.transition_state(ItemState.CHOOSE_RECIPE)
            
            elif self.state == ItemState.CHOOSE_RECIPE:
                if SUPER_ENERGY:
                    primary_item = Items.avantoe_potion_unf
                    secondary_item = Items.mort_myre_fungus
                    qty = 14
                    timeout = 18
                    button = "space"
    
                elif STAMINA:
                    primary_item = Items.super_energy
                    secondary_item = Items.amylase_crystal
                    qty = "all"
                    timeout = 32
                    button = "space"
                    
                elif GLASS_ORB:
                    primary_item = Items.molten_glass
                    secondary_item = Items.glassblowing_pipe
                    qty = "all"
                    timeout = 50
                    button = "6"

                elif CRUSH_BIRDNESTS:
                    primary_item = Items.empty_birdnest
                    secondary_item = Items.pestle_and_mortar
                    qty = "all"
                    timeout = 45
                    button = "space"

                else:
                    self.transition_state(ItemState.FAILED)
                    continue

                self.transition_state(ItemState.WITHDRAW_INGREDIENTS)
                continue
                    
            elif self.state == ItemState.WITHDRAW_INGREDIENTS:
                if not withdraw_if_in_stock(screenshot_of_tab_ii, secondary_item, qty):
                    self.transition_state(ItemState.FAILED)
                    continue

                if not withdraw_if_in_stock(screenshot_of_tab_ii, primary_item, qty):
                    self.transition_state(ItemState.FAILED)
                    continue
                
                press('esc')
                self.transition_state(ItemState.COMBINE_INGREDIENTS)
                continue
            
            elif self.state == ItemState.COMBINE_INGREDIENTS:
                click(wait(template=secondary_item, timeout=1))
                click(wait(template=primary_item, timeout=1))
                sleep(1)
                press(button)
                sleep(timeout)
                self.transition_state(ItemState.SUCCESS)
                continue

            elif self.state == ItemState.SUCCESS:
                return True
            
            elif self.state == ItemState.FAILED:
                return False
