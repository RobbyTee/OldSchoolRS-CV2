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

class StaffStates(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    WITHDRAW_ITEMS = auto()
    MAKE_BATTLESTAFFS = auto()
    ALCH_STAFFS = auto()
    SUCCESS = auto()
    FAILED = auto()


class MakeStaffs():
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)

    def start(self):
        self.transition_state(StaffStates.INIT)

        while True:
            if self.state == StaffStates.INIT:
                self.transition_state(StaffStates.OPEN_BANK)

            elif self.state == StaffStates.OPEN_BANK:
                if not open_bank():
                    state = StaffStates.FAILED
                    log_state(state)
                    continue

                templates = [Bank.deposit_inventory, Bank.deposit_equipment]

                screenshot = capture_runelite_window()
                coords = find_by_templates(templates, screenshot, 
                                            bounds=whole.bounds)
                
                for coord in coords:
                    click(coord)

                log_event("Bank opened and deposited inventory & equipment.")
                self.transition_state(StaffStates.WITHDRAW_ITEMS)