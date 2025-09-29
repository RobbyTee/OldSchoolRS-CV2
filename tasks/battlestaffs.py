from config import STAFF, HIGH_ALCHEMY
from enum import Enum, auto
from pyautogui import press, moveTo, leftClick
from runelite_library.area import play_area, inventory, whole
from runelite_library.bank import open_bank
from runelite_library.check_charges import log_use
from runelite_library.filters import find_by_template, find_by_templates, wait
from runelite_library.interaction import click, right_click, use_rgb1_on_rgb2
from runelite_library.logger import log_event, log_state, read_prev_state
from runelite_library.window_management import capture_runelite_window
from time import sleep
from too_many_items import Pathing, Bank, Items, Menu, Objects, Misc, Runes, Interfaces, Normal_Spellbook

orb_list = {
    "water": Items.water_orb,
    "earth": Items.earth_orb,
    "fire": Items.fire_orb,
    "air": Items.air_orb,
}

ORB = orb_list.get(STAFF)

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
                self.completed_staff = (155, 236, 228)
                self.orb = (34, 144, 133)
                self.battlestaff = (30, 130, 70)
                self.nature_runes = (135, 255, 135)
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

            elif self.state == StaffStates.WITHDRAW_ITEMS:
                bank_screen = capture_runelite_window()

                if HIGH_ALCHEMY:
                    click_tab_all = click(find_by_template(bank_screen, Bank.tab_all))
                    if not click_tab_all:
                        self.transition_state(StaffStates.FAILED)
                        continue

                    click_quantity_all = click(find_by_template(bank_screen, Bank.quantity_all))
                    if not click_quantity_all:
                        self.transition_state(StaffStates.FAILED)
                        continue
                    
                    tab_all = capture_runelite_window()

                    withdraw_nature_runes = click(find_by_template(tab_all, Runes.nature))
                    if not withdraw_nature_runes:
                        self.transition_state(StaffStates.FAILED)
                        continue

                    withdraw_fire_staff = click(find_by_template(tab_all, Items.fire_battlestaff))
                    if not withdraw_fire_staff:
                        self.transition_state(StaffStates.FAILED)
                        continue

                click_tab_vi = click(find_by_template(bank_screen, Bank.tab_vi))
                if not click_tab_vi:
                    self.transition_state(StaffStates.FAILED)
                    continue
                
                tab_vi = capture_runelite_window()

                click_quantity_10 = click(find_by_template(bank_screen, Bank.quantity_10))
                if not click_quantity_10:
                    self.transition_state(StaffStates.FAILED)
                    continue

                withdraw_orb = click(find_by_template(tab_vi, ORB))
                if not withdraw_orb:
                    self.transition_state(StaffStates.FAILED)
                    continue

                withdraw_battlestaff = click(find_by_template(tab_vi, Items.battlestaff))
                if not withdraw_battlestaff:
                    self.transition_state(StaffStates.FAILED)
                    continue
                
                press('esc')
                sleep(1.4)

                inventory_ss = capture_runelite_window()

                click_fire_staff = click(find_by_template(inventory_ss, Items.fire_battlestaff))
                if not click_fire_staff:
                    self.transition_state(StaffStates.FAILED)
                    continue
                
                sleep(1)

                self.transition_state(StaffStates.MAKE_BATTLESTAFFS)
                continue

            elif self.state == StaffStates.MAKE_BATTLESTAFFS:
                inventory_ss = capture_runelite_window()
                use_rgb1_on_rgb2(inventory_ss, self.orb, self.battlestaff)
                
                sleep(1)
                press('space')
                sleep(12)

                if HIGH_ALCHEMY:
                    self.transition_state(StaffStates.ALCH_STAFFS)
                    continue
                else:
                    self.transition_state(StaffStates.SUCCESS)

            elif self.state == StaffStates.ALCH_STAFFS:
                press(Interfaces.spells_icon)

                spellbook = capture_runelite_window()

                click_high_alch = click(find_by_template(spellbook, Normal_Spellbook.high_alch))
                if not click_high_alch:
                    press(Interfaces.inventory_icon)
                    self.transition_state(StaffStates.SUCCESS)
                    continue
                
                alch_battlestaff = click(wait(rgb_color=self.completed_staff, timeout=5))
                if alch_battlestaff:
                    sleep(4)
                else:
                    leftClick()
                    self.transition_state(StaffStates.SUCCESS)
                    continue

            elif self.state == StaffStates.FAILED:
                return False
            
            elif self.state == StaffStates.SUCCESS:
                return True