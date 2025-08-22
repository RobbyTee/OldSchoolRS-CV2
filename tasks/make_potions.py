import pyautogui

from config import (
    RANARR, AVANTOE, SNAPDRAGON, KWUARM
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

class MakeStates(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    WITHDRAW_WATER = auto()
    WITHDRAW_HERB = auto()
    FAILED = auto()
    SET_WITHDRAW_14 = auto()
    COMBINE_INGREDIENTS = auto()
    SUCCESS = auto()

class MakePotion:
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)


    def start(self):
        self.transition_state(MakeStates.INIT)

        while True:
            if self.state == MakeStates.INIT:
                self.transition_state(MakeStates.OPEN_BANK)

            elif self.state == MakeStates.OPEN_BANK:
                # Open bank and empty inventory and equipment
                if open_bank():
                    screenshot = capture_runelite_window()
                    coords = find_by_template(screenshot=screenshot, template_path=Bank.deposit_inventory)
                    if coords:
                        click(coords)
                    else:
                        self.transition_state(MakeStates.FAILED)
                        
                    self.transition_state(MakeStates.WITHDRAW_WATER)
                else:
                    self.transition_state(MakeStates.FAILED)

            elif self.state == MakeStates.WITHDRAW_WATER:
                click(wait(template=Bank.tab_ii))
                if not right_click(wait(template=Items.vial_of_water)):
                    log_event("Out of vials of water!", level="error")
                    return False
                screenshot = capture_runelite_window()
                withdraw_14 = find_by_template(screenshot=screenshot, 
                                               template_path=Bank.withdraw_14)
                if not withdraw_14:
                    self.transition_state(MakeStates.SET_WITHDRAW_14)
                    continue
                else:
                    click(withdraw_14)
                    self.transition_state(MakeStates.WITHDRAW_HERB)

            elif self.state == MakeStates.SET_WITHDRAW_14:
                if not click(wait(template=Bank.withdraw_x)):
                    self.transition_state(MakeStates.FAILED)
                    continue
                sleep(2)
                press('1')
                press('4')
                press('enter')
                self.transition_state(MakeStates.WITHDRAW_HERB)

            elif self.state == MakeStates.WITHDRAW_HERB:
                screenshot = capture_runelite_window()
                if RANARR:
                    coords = find_by_template(screenshot=screenshot,
                                              template_path=Items.clean_ranarr)
                    moveTo(coords)
                    herb_exists = wait(template=Misc.good, bounds=play_area.bounds, 
                                       timeout=1)
                    if herb_exists:
                        pyautogui.rightClick()
                        click(wait(template=Bank.withdraw_14))
                        self.transition_state(MakeStates.COMBINE_INGREDIENTS)
                        continue
                    else:
                        pass
                    
                if AVANTOE:
                    coords = find_by_template(screenshot=screenshot,
                                              template_path=Items.clean_avanatoe)
                    moveTo(coords)
                    herb_exists = wait(template=Misc.good, bounds=play_area.bounds, 
                                       timeout=1)
                    if herb_exists:
                        pyautogui.rightClick()
                        click(wait(template=Bank.withdraw_14))
                        self.transition_state(MakeStates.COMBINE_INGREDIENTS)
                        continue
                    else:
                        pass

                if KWUARM:
                    coords = find_by_template(screenshot=screenshot,
                                              template_path=Items.clean_kwuarm)
                    moveTo(coords)
                    herb_exists = wait(template=Misc.good, bounds=play_area.bounds, 
                                       timeout=1)
                    if herb_exists:
                        pyautogui.rightClick()
                        click(wait(template=Bank.withdraw_14))
                        self.transition_state(MakeStates.COMBINE_INGREDIENTS)
                        continue
                    else:
                        pass

                if SNAPDRAGON:
                    coords = find_by_template(screenshot=screenshot,
                                              template_path=Items.clean_snapdragon)
                    moveTo(coords)
                    herb_exists = wait(template=Misc.good, bounds=play_area.bounds, 
                                       timeout=1)
                    if herb_exists:
                        pyautogui.rightClick()
                        click(wait(template=Bank.withdraw_14))
                        self.transition_state(MakeStates.COMBINE_INGREDIENTS)
                        continue
                    else:
                        pass
                
                log_event("Out of herbs!")
                self.transition_state(MakeStates.FAILED)
                continue
            
            elif self.state == MakeStates.COMBINE_INGREDIENTS:
                clean_herb = (89, 40, 200)
                press('esc')
                if not click(wait(rgb_color=clean_herb)):
                    log_event("Tried to click on herb in inventory, but failed!")
                    self.transition_state(MakeStates.FAILED)
                    continue
                if not click(wait(template=Items.vial_of_water, bounds=inventory.bounds)):
                    log_event("Tried to click on vial of water in inventory, but failed!")
                    self.transition_state(MakeStates.FAILED)
                    continue
                sleep(1)
                press('space')
                sleep(10)
                self.transition_state(MakeStates.SUCCESS)
                
            elif self.state == MakeStates.SUCCESS:
                return True

            elif self.state == MakeStates.FAILED:
                press('esc')
                return False