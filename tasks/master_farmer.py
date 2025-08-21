import numpy as np

from enum import Enum, auto
from pyautogui import press
from runelite_library.area import whole, minimap, inventory, play_area
from runelite_library.bank import open_bank
from runelite_library.check_charges import log_use
from runelite_library.filters import (find_by_template, find_by_templates, 
                                      wait, area_by_color, find_by_cic, 
                                      find_by_color, find_all_by_color)
from runelite_library.interaction import (click, right_click, use_rgb1_on_rgb2, 
                                          use_rgb_on_template)
from runelite_library.inventory import avg_color_in_last_inventory
from runelite_library.logger import log_event, log_state, read_prev_state
from runelite_library.player_stats import current_health
from runelite_library.window_management import capture_runelite_window
from time import sleep, time
from too_many_items import (Pathing, Bank, Items, Menu, Global_Colors,
            Misc, Interfaces, Normal_Spellbook, Armor, Food, Runes,
            Player)


class FarmerStates(Enum):
    INIT = auto()
    CLICK_FARMER = auto()
    DETERMINE_LOCATION = auto()
    EAT_FOOD = auto()
    EMPTY_INVENTORY = auto()
    FAILED = auto()
    FIND_VALID_WORLD = auto()
    GEAR_UP = auto()
    OPEN_BANK = auto()
    OPEN_DOOR = auto()
    RETURN_TO_BANK = auto()
    SUCCESS = auto()
    TELEPORT_TO_HOUSE = auto()
    WAIT_FOR_FARMER_IN_POSITION = auto()
    WALK_TO_FARMER_FROM_HOUSE = auto()
    WALK_TO_FARMER_FROM_BANK = auto()
    

class Pickpocket:
    def transition_state(self, transition_to_state):
        self.state = transition_to_state
        log_state(self.state)


    def teleport_outside_house(self):
        press(Interfaces.spells_icon)
        screenshot = capture_runelite_window()
        if not right_click(find_by_template(screenshot, Normal_Spellbook.house_tele)):
            return False
        if not click(wait(template=Menu.outside)):
            return False
        sleep(3)
        press(Interfaces.inventory_icon)
        return True


    def click_rogues_outfit(self, bounds):
        screenshot = capture_runelite_window()
        rogues_pieces = [Armor.rogue_boots, Armor.rogue_gloves, Armor.rogue_mask,
                        Armor.rogue_top, Armor.rogue_trousers]
        rouges_outfit = find_by_templates(template_paths=rogues_pieces,
                                            screenshot=screenshot,
                                            bounds=bounds)
        for piece in rouges_outfit:
            click(piece)


    def open_door(self):
        door = (150, 50, 200)
        closed_door = wait(rgb_color=door, timeout=0.5)
        if closed_door:
            click(closed_door)
            sleep(3)


    def empty_inventory(self, screenshot):
        if not self.prev_time:
            pass
        elif time() - self.prev_time < 10:
            return False
        
        bad_seed = (75, 0, 0)
        bad_seeds = find_all_by_color(bad_seed, screenshot, bounds=inventory.bounds)
        
        for seed in bad_seeds:
            click(seed)
        
        sleep(2)
        self.prev_time = time()
        
        return True


    def player_position(self):
        return wait(Player.player_tile, bounds=play_area.bounds)
    

    def did_player_move(self):
        self.player_position_tolerance = 20
        self.current_player_position = wait(Player.player_tile)
        if self.current_player_position:
            x, y = self.current_player_position
        else:
            return False

        dist = np.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2)
        if dist > self.player_position_tolerance:
            sleep(5)
            self.initial_player_position = self.player_position()
            self.x0, self.y0 = self.initial_player_position
            return True
        else:
            return False


    def start(self):
        self.state = FarmerStates.INIT

        while True:
            if self.state == FarmerStates.INIT:
                log_event("Starting master_farmer.py task!")
                self.master_farmer = (0, 255, 255)
                self.prev_time = None
                self.transition_state(FarmerStates.DETERMINE_LOCATION)

            elif self.state == FarmerStates.DETERMINE_LOCATION:
                at_hosidius = False
                hosidius_bank = wait(template=Bank.hosidius, timeout=1)
                
                if hosidius_bank:
                    log_event("Starting at the Hosidius bank.", "debug")
                    at_hosidius = True
                else:
                    log_event("Not starting in Hosidius.", "debug")
                self.transition_state(FarmerStates.OPEN_BANK)

            elif self.state == FarmerStates.OPEN_BANK:
                # Open bank and empty inventory and equipment
                if open_bank():
                    templates = [Bank.deposit_equipment, Bank.deposit_inventory]
                    screenshot = capture_runelite_window()
                    coords = find_by_templates(templates, screenshot, 
                                               bounds=whole.bounds)
                    
                    for coord in coords:
                        click(coord)
                    
                    self.transition_state(FarmerStates.GEAR_UP)
                else:
                    self.transition_state(FarmerStates.FAILED)

            elif self.state == FarmerStates.GEAR_UP:
                # Tab iii & withdraw 1
                click(wait(template=Bank.tab_iii))
                
                try:
                    click(wait(template=Bank.quantity_1, template_tol=0.6))
                except:
                    pass

                self.click_rogues_outfit(bounds=play_area.bounds)
                
                # click(wait(template=Items.seed_box))

                # Tab VI and quantity 5
                click(wait(template=Bank.tab_vi))
                click(wait(template=Bank.quantity_5))

                click(wait(template=Food.lobster))

                # Tab ALL & quantity 1
                click(wait(template=Bank.tab_all))
                
                try:
                    click(wait(template=Bank.quantity_1, template_tol=0.6))
                except:
                    pass

                click(wait(template=Armor.ardougne_cloak))

                if not at_hosidius:
                    click(wait(template=Runes.air))
                    click(wait(template=Runes.law))
                    click(wait(template=Runes.earth))
                    self.transition_state(FarmerStates.TELEPORT_TO_HOUSE)
                
                else:
                    self.transition_state(FarmerStates.WALK_TO_FARMER_FROM_BANK)
                
                press('esc')
                sleep(1)
                self.click_rogues_outfit(bounds=inventory.bounds)
                click(wait(template=Armor.ardougne_cloak, bounds=inventory.bounds))

            elif self.state == FarmerStates.TELEPORT_TO_HOUSE:
                press(Interfaces.spells_icon)
                right_click(wait(template=Normal_Spellbook.house_tele))
                click(wait(template=Menu.outside))
                press(Interfaces.inventory_icon)
                sleep(3)

                self.transition_state(FarmerStates.WALK_TO_FARMER_FROM_HOUSE)

            elif self.state == FarmerStates.WALK_TO_FARMER_FROM_HOUSE:
                bounds = minimap.bounds
                click(wait(rgb_color=Pathing.step_1, bounds=bounds))
                click(wait(rgb_color=Pathing.step_2, bounds=bounds))
                click(wait(rgb_color=Pathing.step_3, bounds=bounds))
                click(wait(rgb_color=Pathing.step_4, bounds=bounds))
                click(wait(rgb_color=Pathing.step_5, bounds=bounds))
                click(wait(rgb_color=Pathing.step_6, bounds=bounds))
                click(wait(rgb_color=Pathing.step_7, bounds=bounds))
                click(wait(rgb_color=Pathing.step_8, bounds=bounds))
                click(wait(rgb_color=Pathing.step_9, bounds=bounds))
                click(wait(rgb_color=Pathing.step_10, bounds=bounds))
                sleep(6)
                self.open_door()
                click(wait(Pathing.step_1, bounds=minimap.bounds))
                sleep(3)
                self.transition_state(FarmerStates.FIND_VALID_WORLD)
            
            elif self.state == FarmerStates.WALK_TO_FARMER_FROM_BANK:
                bounds = minimap.bounds
                click(wait(rgb_color=Pathing.step_7, bounds=bounds))
                click(wait(rgb_color=Pathing.step_8, bounds=bounds))
                click(wait(rgb_color=Pathing.step_9, bounds=bounds))
                click(wait(rgb_color=Pathing.step_10, bounds=bounds))
                sleep(6)
                self.open_door()
                click(wait(Pathing.step_1, bounds=minimap.bounds))
                sleep(3)
                self.transition_state(FarmerStates.FIND_VALID_WORLD)

            elif self.state == FarmerStates.FIND_VALID_WORLD:
                log_event("Finding valid world")
                self.house = (255, 0, 255)
                screenshot = capture_runelite_window()
                house_bounds = area_by_color(self.house, screenshot, bounds=play_area.bounds)
                farmer_in_house = wait(self.master_farmer, bounds=house_bounds, timeout=5)
                if farmer_in_house:
                    log_event("Found a valid world")
                    self.transition_state(FarmerStates.WAIT_FOR_FARMER_IN_POSITION)
                    continue
                else:
                    log_event("Hopping worlds.", "debug")
                    press('u')
                    sleep(10)
                    continue
            
            elif self.state == FarmerStates.WAIT_FOR_FARMER_IN_POSITION:
                log_event("Waiting for farmer to get in position.")
                
                press(Interfaces.inventory_icon)
                timeout = 30    # seconds
                
                self.initial_player_position = self.player_position()
                self.x0, self.y0 = self.initial_player_position
                
                farmer_in_position = False
                self.start = time()

                while True:
                    screenshot = capture_runelite_window()
                    farmer_in_a_square = find_by_cic(self.master_farmer, 
                                                    self.house, 
                                                    screenshot,
                                                    bounds=play_area.bounds)
                    if farmer_in_a_square:
                        farmer_in_position = True
                        break
                    else:    
                        if time() - self.start > timeout:
                            log_event("Timed out waiting for Master Farmer to get into position.", "warning")
                            break
                
                if farmer_in_position:
                    self.transition_state(FarmerStates.CLICK_FARMER)
                    continue
                else:
                    self.transition_state(FarmerStates.FIND_VALID_WORLD)
                    continue

            elif self.state == FarmerStates.CLICK_FARMER:
                screenshot = capture_runelite_window()

                if find_by_color(rgb_color=(200, 0, 150), screenshot=screenshot,
                                 bounds=play_area.bounds):
                    # If we end up upstairs, click the ladder
                    ladder = wait((50, 50, 200), timeout=1)
                    x,y = ladder
                    click((x+20,y))
                    sleep(3)
                    continue

                farmer = find_by_cic(self.master_farmer, 
                                    self.house, 
                                    screenshot,
                                    bounds=play_area.bounds,
                                    tolerance=10)
                
                if self.did_player_move():
                    continue

                if find_by_template(screenshot, Misc.stunned):
                    log_event("    Stunned", "debug")
                    sleep(4)
                    continue

                last_inv_slot = avg_color_in_last_inventory(screenshot)
                if last_inv_slot != Global_Colors.last_inv:
                    log_event("    Inventory full", "debug")
                    if self.empty_inventory(screenshot):
                        continue
                    else:
                        log_event("    Inventory too full to continue", "debug")
                        self.transition_state(FarmerStates.RETURN_TO_BANK)
                        continue

                health = current_health(screenshot)
                if health != Player.most_health:
                    self.transition_state(FarmerStates.EAT_FOOD)
                    continue

                if farmer:
                    log_event("    Clicked farmer", "debug")
                    click(farmer)
                    continue
                else:
                    log_event("    Farmer isn't in a good position", "debug")
                    self.transition_state(FarmerStates.WAIT_FOR_FARMER_IN_POSITION)
                    continue

            elif self.state == FarmerStates.EAT_FOOD:
                log_event("The flesh is weak! I need sustainance.", "debug")
                if not click(wait(Global_Colors.food, bounds=inventory.bounds)):
                    log_event("No more food to eat, must restock!", "debug")
                    self.transition_state(FarmerStates.RETURN_TO_BANK)
                    continue
                else:
                    self.transition_state(FarmerStates.CLICK_FARMER)
                    continue
            
            elif self.state == FarmerStates.RETURN_TO_BANK:
                log_event("Returning to bank.")
                self.open_door()

                bounds = minimap.bounds
                click(wait(Pathing.step_10, bounds=bounds))
                click(wait(Pathing.step_9, bounds=bounds))
                click(wait(Pathing.step_8, bounds=bounds))
                click(wait(Pathing.step_7, bounds=bounds))
                click(wait(Bank.bank_floor, bounds=bounds))
                sleep(6)

                screenshot = capture_runelite_window()
                self.empty_inventory(screenshot)
                
                self.transition_state(FarmerStates.SUCCESS)
                continue

            elif self.state == FarmerStates.SUCCESS:
                log_event("Successfully completed a trip to the Master Farmer.")
                return True

            elif self.state == FarmerStates.FAILED:
                log_event("Failed to pickpocket farmer!")
                return False