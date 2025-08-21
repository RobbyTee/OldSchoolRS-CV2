from enum import Enum, auto
from pyautogui import press
from runelite_library.area import whole, minimap, play_area, inventory
from runelite_library.bank import open_bank
from runelite_library.filters import wait, find_by_template, find_by_templates, find_by_color
from runelite_library.interaction import click, get_worn_equipment, right_click
from runelite_library.inventory import avg_color_in_last_inventory
from runelite_library.logger import log_event, log_state, read_prev_state
from runelite_library.window_management import capture_runelite_window
from time import sleep
from too_many_items import (Armor, Bank, Global_Colors, Items, 
        Menu, Misc, Pathing, Interfaces)


class MortMyreStates(Enum):
    INIT = auto()
    FAILED = auto()
    FARM_FUNGI = auto()
    GEAR_UP = auto()
    OPEN_BANK = auto()
    NAVIGATE_TO_CANIFIS = auto()
    RECHARGE_PRAYER = auto()
    SUCCESS = auto()
    TELPORT_TO_MONASTERY = auto()
    TELEPORT_TO_CASTLE_WARS = auto()
    WALK_TO_STUMPS = auto()
    


class Fungus:
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)

    
    def start(self):
        self.state = MortMyreStates.INIT
        
        while True:
            if self.state == MortMyreStates.INIT:
                self.transition_state(MortMyreStates.OPEN_BANK)
            
            elif self.state == MortMyreStates.OPEN_BANK:
                    # Open bank and empty inventory and equipment
                    if open_bank():
                        templates = [Bank.deposit_equipment, Bank.deposit_inventory]
                        screenshot = capture_runelite_window()
                        coords = find_by_templates(templates, screenshot, 
                                                bounds=whole.bounds)
                        
                        for coord in coords:
                            click(coord)
                        
                        self.transition_state(MortMyreStates.GEAR_UP)
                    else:
                        self.transition_state(MortMyreStates.FAILED)
            
            elif self.state == MortMyreStates.GEAR_UP:
                # Tab iii & withdraw 1
                click(wait(template=Bank.tab_all))
                
                try:
                    click(wait(template=Bank.quantity_1, template_tol=0.6))
                except:
                    pass

                click(wait(template=Armor.ardougne_cloak))
                if not click(wait(template=Items.ring_of_dueling)):
                    self.transition_state(MortMyreStates.FAILED)
                    continue

                click(wait(template=Items.dramen_staff))

                click(wait(template=Bank.tab_iii))
                click(wait(template=Items.sickle))

                press('esc')
                sleep(2)

                bounds = inventory.bounds
                click(wait(template=Armor.ardougne_cloak, bounds=bounds))
                click(wait(template=Items.ring_of_dueling, bounds=bounds))
                click(wait(template=Items.dramen_staff, bounds=bounds))
                
                self.transition_state(MortMyreStates.TELPORT_TO_MONASTERY)

            elif self.state == MortMyreStates.TELPORT_TO_MONASTERY:
                press(Interfaces.equipment_icon)
                right_click(wait(template=Armor.ardougne_cloak))
                click(wait(template=Menu.monastery))
                sleep(3)
                press(Interfaces.inventory_icon)
                self.transition_state(MortMyreStates.RECHARGE_PRAYER)

            elif self.state == MortMyreStates.RECHARGE_PRAYER:
                click(wait(Pathing.step_10, bounds=minimap.bounds))
                sleep(6)
                click(wait(Global_Colors.altar))
                sleep(5)
                self.transition_state(MortMyreStates.NAVIGATE_TO_CANIFIS)

            elif self.state == MortMyreStates.NAVIGATE_TO_CANIFIS:
                bounds = minimap.bounds
                click(wait(Pathing.step_1, bounds=bounds))
                click(wait(Pathing.step_2, bounds=bounds))
                click(wait(Pathing.step_3, bounds=bounds))
                click(wait(Pathing.step_4, bounds=bounds))
                click(wait(Pathing.step_5, bounds=bounds))
                click(wait(Pathing.step_6, bounds=bounds))
                sleep(5)

                click(wait(Global_Colors.fairy_ring))
                sleep(5)
                self.transition_state(MortMyreStates.WALK_TO_STUMPS)

            elif self.state == MortMyreStates.WALK_TO_STUMPS:
                gate = (134, 238, 87)

                bounds = minimap.bounds
                click(wait(Pathing.step_1, bounds=bounds))
                sleep(6)
                if not click(wait(gate)):
                    self.transition_state(MortMyreStates.FAILED)
                    continue
                sleep(4)

                click(wait(Pathing.step_2, bounds=bounds))
                sleep(6)
                click(wait(Pathing.step_3, bounds=bounds))
                sleep(6)

                self.transition_state(MortMyreStates.FARM_FUNGI)

            elif self.state == MortMyreStates.FARM_FUNGI:
                fungi_color = (70, 250, 70)
                
                screenshot = capture_runelite_window()
                if avg_color_in_last_inventory(screenshot) != Global_Colors.last_inv:
                    self.transition_state(MortMyreStates.TELEPORT_TO_CASTLE_WARS)
                    continue
                
                click(wait(template=Items.sickle))
                sleep(2)
                while True:
                    screenshot = capture_runelite_window()
                    if avg_color_in_last_inventory(screenshot) != Global_Colors.last_inv:
                        break

                    fungi = wait(fungi_color, bounds=play_area.bounds, timeout=0.5)
                    if not fungi:
                        break
                    else:
                        click(fungi)
                        sleep(3)
                    
                click(wait(Pathing.step_3, bounds=minimap.bounds))
                sleep(2)

            elif self.state == MortMyreStates.TELEPORT_TO_CASTLE_WARS:
                press(Interfaces.equipment_icon)
                right_click(wait(template=Items.ring_of_dueling))
                click(wait(template=Menu.castle_wars))
                sleep(3)
                press(Interfaces.inventory_icon)
                
                click(wait(Bank.bank_floor, bounds=minimap.bounds))
                sleep(6)
                self.transition_state(MortMyreStates.SUCCESS)

            elif self.state == MortMyreStates.SUCCESS:
                return True
            
            elif self.state == MortMyreStates.FAILED:
                return False





