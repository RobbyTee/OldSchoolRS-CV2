from config import STAFF, HIGH_ALCHEMY
from enum import Enum, auto
from pyautogui import press, moveTo
from runelite_library.area import play_area, inventory, whole, minimap
from runelite_library.bank import open_bank, withdraw_skills_necklace
from runelite_library.check_charges import log_use
from runelite_library.filters import wait, find_all_by_template
from runelite_library.interaction import click, right_click
from runelite_library.logger import log_event, log_state
from runelite_library.teleports import TeleportJewlery
from runelite_library.window_management import capture_runelite_window
from time import sleep
from too_many_items import Pathing, Bank, Items, Menu, Objects, Misc

import random

SEED_VAULT = (62,173,124)
# Make this a dictionary of sapling: time_to_harvest
NORMAL_SAPLINGS = {
    Menu.willow_sapling: 240,
    Menu.maple_sapling: 320,
    Menu.yew_sapling: 400,
    Menu.magic_sapling: 480
}

SAPLING_COLOR = (101, 149, 39)

class TreeStates(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    TELEPORT_TO_FARMING_GUILD = auto()
    OPEN_SEED_VAULT = auto()
    WITHDRAW_SAPLINGS = auto()
    CHECK_INVENTORY = auto()
    SUCCESS = auto()
    FAILED = auto()


class TreeRun():
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)

    def start(self):
        self.state = TreeStates.INIT

        while True:
            if self.state == TreeStates.INIT:
                at_guild = wait(template=Bank.farming_guild)
                self.transition_state(TreeStates.OPEN_BANK)
                continue


            elif self.state == TreeStates.OPEN_BANK:
                if not open_bank():
                    state = TreeStates.FAILED
                    log_state(state)
                    continue

                templates = [Bank.deposit_inventory, Bank.deposit_equipment]

                for template in templates:
                    if not click(wait(template=template, timeout=0.5)):
                        state = TreeStates.FAILED
                        log_state(state)
                        continue

                log_event("Bank opened and deposited inventory & equipment.")
                if at_guild:
                    press('esc')
                    sleep(2)
                    self.transition_state(TreeStates.OPEN_SEED_VAULT)
                    continue
                
                else:
                    self.transition_state(TreeStates.TELEPORT_TO_FARMING_GUILD)
                    continue


            elif self.state == TreeStates.TELEPORT_TO_FARMING_GUILD:
                # Withdraw a skills necklace
                withdraw_skills_necklace()

                press('esc')
                
                sleep(2)

                TeleportJewlery().skills_necklace("farming_guild")

                steps_to_bank = [
                    Pathing.step_2, Pathing.step_3
                ]
                for color in steps_to_bank:
                    if not click(wait(rgb_color=color, bounds=minimap.bounds)):
                        exit(1)
                    sleep(3)

                sleep(random.uniform(3, 6))

                self.transition_state(TreeStates.OPEN_SEED_VAULT)
                continue
            
            
            elif self.state == TreeStates.OPEN_SEED_VAULT:
                click(wait(rgb_color=SEED_VAULT))
                click(wait(template=Menu.saplings))
                self.transition_state(TreeStates.WITHDRAW_SAPLINGS)
                continue


            elif self.state == TreeStates.WITHDRAW_SAPLINGS:
                try:
                    sapling = next(iter(NORMAL_SAPLINGS))
                except IndexError:
                    log_event("All out of saplings")
                    #print("Out of saplings")
                    return False
                    
                sapling_coordinates = wait(template=sapling)
                right_click(sapling_coordinates)
                
                if click(wait(template=Bank.withdraw_5, timeout=0.5)):
                    sleep(2)
                    self.transition_state(TreeStates.CHECK_INVENTORY)
                    continue
                else:
                    x,y = sapling_coordinates
                    new_coords = (x + random.uniform(80,160), y + random.uniform(80,160))
                    moveTo(new_coords)
                    sleep(1)
                    NORMAL_SAPLINGS.pop(sapling)
                    continue


            elif self.state == TreeStates.CHECK_INVENTORY:
                screenshot = capture_runelite_window()
                sapling_count = len(find_all_by_template(screenshot=screenshot,
                                                         template_path=Items.sapling,
                                                         bounds=inventory.bounds))
                #print(f"Saplings in inventory = {sapling_count}")
                if sapling_count < 5:
                    NORMAL_SAPLINGS.pop(sapling)
                    click(wait(template=Bank.deposit_inventory))
                    self.transition_state(TreeStates.WITHDRAW_SAPLINGS)
                    continue

                self.transition_state(TreeStates.SUCCESS)
                continue
                

            elif self.state == TreeStates.SUCCESS:
                print("Done")
                log_event("Completed successfully")
                log_state(self.state)
                exit(0)


            elif self.state == TreeStates.FAILED:
                log_event("Something went wrong")
                log_state(self.state)
                exit(1)            