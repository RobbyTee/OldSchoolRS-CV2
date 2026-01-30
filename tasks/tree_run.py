from config import STAFF, HIGH_ALCHEMY
from enum import Enum, auto
from pyautogui import press, moveTo
from runelite_library.area import play_area, inventory, whole, minimap
from runelite_library.bank import open_bank
from runelite_library.check_charges import log_use
from runelite_library.filters import wait
from runelite_library.interaction import click, right_click
from runelite_library.logger import log_event, log_state
from runelite_library.farming_guild import withdraw_skills_necklace, farming_guild_teleport
from time import sleep
from too_many_items import Pathing, Bank, Items, Menu, Objects, Misc

import random

SEED_VAULT = (62,173,124)

class TreeStates(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    TELEPORT_TO_FARMING_GUILD = auto()
    WITHDRAW_SAPLINGS = auto()
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
                self.transition_state(TreeStates.OPEN_BANK)

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
                self.transition_state(TreeStates.TELEPORT_TO_FARMING_GUILD)

            elif self.state == TreeStates.TELEPORT_TO_FARMING_GUILD:
                # Withdraw a skills necklace
                withdraw_skills_necklace()

                press('esc')
                
                sleep(2)

                farming_guild_teleport()

                steps_to_bank = [
                    Pathing.step_2, Pathing.step_3
                ]
                for color in steps_to_bank:
                    if not click(wait(rgb_color=color, bounds=minimap.bounds)):
                        exit(1)
                    sleep(3)

                sleep(random.uniform(3, 6))

                self.transition_state(TreeStates.WITHDRAW_SAPLINGS)
                continue
                        
            elif self.state == TreeStates.WITHDRAW_SAPLINGS:
                click(wait(rgb_color=SEED_VAULT))
                click(wait(template=Menu.saplings))
                self.transition_state(TreeStates.SUCCESS)
                continue


            elif self.state == TreeStates.SUCCESS:
                log_event("Completed successfully")
                log_state(self.state)
                exit(0)

            elif self.state == TreeStates.FAILED:
                log_event("Something went wrong")
                log_state(self.state)
                exit(1)            