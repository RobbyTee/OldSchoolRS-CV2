from config import (
    ARDOUGNE_CLOAK, CLOAK_MAX_USES,
    EXPLORERS_RING, RING_MAX_USES,
    MAGIC_SECATEURS, RAKE
)
from enum import Enum, auto
from pyautogui import press, moveTo, leftClick
from runelite_library.area import whole, minimap, inventory, play_area
from runelite_library.bank import open_bank
from runelite_library.check_charges import check_charges
from runelite_library.check_charges import log_use
from runelite_library.filters import (find_by_template, find_by_templates, 
                                    wait, find_by_color, find_all_by_color)
from runelite_library.interaction import (click, right_click)
from runelite_library.inventory import avg_color_in_last_inventory
from runelite_library.logger import log_event, log_state
from runelite_library.window_management import capture_runelite_window
from time import sleep, time
from too_many_items import (
    Armor, Pathing, Bank, Items, Menu, Misc, Runes, Interfaces,
    Normal_Spellbook, Global_Colors)


class FarmStates(Enum):
    INIT = auto()
    CHECK_STATUS_OF_TELEPORTS = auto()
    OPEN_BANK = auto()
    GEAR_UP = auto()
    # Traveling
    GO_TO_NEXT_FARM = auto()
    NAVIGATE_TO_HOSIDIUS = auto()
    NAVIGATE_TO_CATHERBY = auto()
    NAVIGATE_TO_FALADOR = auto()
    NAVIGATE_TO_ARDOUGNE = auto()
    NAVIGATE_TO_FARMING_GUILD = auto()
    # Harvesting
    HARVEST_HERB = auto()
    HARVEST_FLOWER = auto()
    HARVESTING = auto()
    CLEAN_HERBS = auto()
    TURN_INTO_NOTES = auto()
    # Planting
    PLANT_SEED = auto()
    COMPOST = auto()
    # Error
    FAILED = auto()
    # SUCCESS
    FINISH_AT_BANK = auto()
    SUCCESS = auto()


class FarmRun:
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
    

    def walk_to_hosidius_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        if not click(wait(Pathing.step_1, bounds=bounds)):
            return False
        if not click(wait(Pathing.step_2, bounds=bounds)):
            return False
        if not click(wait(Pathing.step_3, bounds=bounds)):
            return False
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False


    def teleport_to_camelot(self):
        press(Interfaces.spells_icon)
        screenshot = capture_runelite_window()
        if not click(find_by_template(screenshot, Normal_Spellbook.camelot_tele)):
            return False
        press(Interfaces.inventory_icon)
        return True


    def walk_to_catherby_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        click(wait(Pathing.step_1, bounds=bounds))
        click(wait(Pathing.step_2, bounds=bounds))
        click(wait(Pathing.step_3, bounds=bounds))
        click(wait(Pathing.step_4, bounds=bounds))
        click(wait(Pathing.step_5, bounds=bounds))
        click(wait(Pathing.step_6, bounds=bounds))
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False


    def teleport_to_ardougne(self):
        press(Interfaces.spells_icon)
        if not click(wait(template=Normal_Spellbook.ardy_tele)):
            return False
        sleep(3)
        press(Interfaces.inventory_icon)
        return True
    

    def teleport_with_cloak(self):
        if not right_click(wait(template=Armor.ardougne_cloak, bounds=inventory.bounds)):
            return False
        if not click(wait(template=Menu.farm)):
            return False
        sleep(3)
        log_use("ardougne_cloak")
        return True
    

    def walk_to_ardougne_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        click(wait(Pathing.step_8, bounds=bounds))
        click(wait(Pathing.step_1, bounds=bounds))
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False
        

    def long_walk_to_ardougne_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        click(wait(Pathing.step_1, bounds=bounds))
        click(wait(Pathing.step_2, bounds=bounds))
        click(wait(Pathing.step_3, bounds=bounds))
        click(wait(Pathing.step_4, bounds=bounds))
        click(wait(Pathing.step_5, bounds=bounds))
        click(wait(Pathing.step_6, bounds=bounds))
        click(wait(Pathing.step_7, bounds=bounds))
        click(wait(Pathing.step_8, bounds=bounds))
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False


    def teleport_to_falador(self):
        press(Interfaces.spells_icon)
        if not click(wait(template=Normal_Spellbook.falador_tele)):
            return False
        sleep(3)
        press(Interfaces.inventory_icon)
        return True


    def teleport_with_ring(self):
        if not right_click(wait(template=Items.explorers_ring, bounds=inventory.bounds)):
            return False
        if not click(wait(template=Menu.teleport)):
            return False
        log_use("explorers_ring")
        return True


    def walk_to_falador_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        click(wait(Pathing.step_1, bounds=bounds))
        click(wait(Pathing.step_2, bounds=bounds))
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False


    def long_walk_to_falador_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        click(wait(Pathing.step_1, bounds=bounds))
        click(wait(Pathing.step_2, bounds=bounds))
        click(wait(Pathing.step_3, bounds=bounds))
        click(wait(Pathing.step_4, bounds=bounds))
        click(wait(Pathing.step_5, bounds=bounds))
        click(wait(Pathing.step_6, bounds=bounds))
        click(wait(Pathing.step_7, bounds=bounds))
        click(wait(Pathing.step_8, bounds=bounds))
        click(wait(Pathing.step_9, bounds=bounds))
        click(wait(Pathing.step_10, bounds=bounds))
        click(wait(Pathing.step_2, bounds=bounds))
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False


    def teleport_with_necklace(self):
        if not right_click(wait(template=Items.skills_necklace, bounds=inventory.bounds)):
            return False
        if not click(wait(template=Menu.rub)):
            return False
        sleep(1)
        press('6')
        sleep(3)
        return True
    

    def walk_to_guild_patch(self):
        herb_tile = (135, 255, 0)
        bounds = minimap.bounds
        click(wait(Pathing.step_1, bounds=bounds))
        sleep(6)
        if wait(herb_tile, bounds=play_area.bounds):
            return True
        else:
            return False


    def harvesting(self):
        empty_patch = (70, 250, 70)
        now = time()
        time_limit = 30
        while time() - now < time_limit:
            screenshot = capture_runelite_window()
            if find_by_color(empty_patch, screenshot, bounds=play_area.bounds):
                return True
            if avg_color_in_last_inventory(screenshot) != Global_Colors.last_inv:
                return False
    
        return False
    

    def clean_herbs(self):
        grimy_herb = (40, 240, 120)
        screenshot = capture_runelite_window()
        grimy_herbs = (find_all_by_color(grimy_herb, screenshot, bounds=inventory.bounds))
        if not grimy_herbs:
            return False # Dead!
        for herb in grimy_herbs:
            click(herb)
        return True


    def check_stock(self, screenshot, item):
        """
        Input screenshot and template path of item. It'll hover over it and check
        if "GOOD" pops up. Used mostly with the bank.
        """
        item_to_withdraw = find_by_template(screenshot, item)
        
        if item_to_withdraw:
            moveTo(item_to_withdraw)
        else:
            log_event(f"No {str(item)} in stock!", level="error")
            return False, None
        
        enough_in_stock = wait(template=Misc.good, bounds=play_area.bounds, timeout=1)
        
        if enough_in_stock:         
            return True, item_to_withdraw
        else:
            log_event(f"Not enough {str(item)} in stock.", level="error")
            return False, None


    def start(self, start_state=FarmStates.INIT):
        self.transition_state(start_state)

        while True:
            if self.state == FarmStates.INIT:
                log_event("Starting farm run!")
                farm = 1 # Start with Hosidius and count up
                # Farm area
                self.empty_patch = (70, 250, 70)
                self.herb_tile = (135, 255, 0)
                self.flower_patch = (255, 240, 90)
                self.flower_tile = (200, 255, 0)
                self.tool_leprechaun = (255, 200, 80)
                self.crossover_area = (64, 110, 39)

                # Inventory
                self.grimy_herb = (40, 240, 120)
                self.herb_seed = (0, 70, 21)
                self.clean_herb = (89, 40, 200)
                self.limpwurt_root = (200, 255, 0)
                self.bottomless_compost = (150, 140, 40)
                
                self.transition_state(FarmStates.CHECK_STATUS_OF_TELEPORTS)
            
            elif self.state == FarmStates.CHECK_STATUS_OF_TELEPORTS:
                if ARDOUGNE_CLOAK:
                    ardy_cloak = check_charges('ardougne_cloak')
                    if ardy_cloak < CLOAK_MAX_USES:
                        log_event("Ardougne Cloak has low charges.")
                        ardougne_cloak = False
                    else:
                        log_event("Ardougne Cloak is ready to use.")
                        ardougne_cloak = True
                else:
                    ardougne_cloak = False
                
                if EXPLORERS_RING:
                    ring = check_charges('explorers_ring')
                    explorers_ring = False
                    if ring < RING_MAX_USES:
                        explorers_ring = True
                        log_event("Using Explorers Ring")
                    else:
                        log_event("Explorers Ring has low charges.")
                        explorers_ring = False
                else:
                    explorers_ring = False

                self.transition_state(FarmStates.OPEN_BANK)

            elif self.state == FarmStates.OPEN_BANK:
                if not open_bank():
                    state = FarmStates.FAILED
                    log_state(state)
                    continue

                templates = [Bank.deposit_inventory, Bank.deposit_equipment]

                screenshot = capture_runelite_window()
                coords = find_by_templates(templates, screenshot, 
                                            bounds=whole.bounds)
                
                for coord in coords:
                    click(coord)

                log_event("Bank opened and deposited inventory & equipment.")
                self.transition_state(FarmStates.GEAR_UP)

            elif self.state == FarmStates.GEAR_UP:
                # Tab iii & quantity 1
                click(wait(template=Bank.tab_iii))
                try:
                    click(wait(template=Bank.quantity_1, template_tol=0.6,
                            timeout=0.5))
                except:
                    log_event('Already on "Withdraw 1" in bank.')
                    pass
                
                tab_iii = capture_runelite_window()
                templates = [Items.spade, Items.seed_dibber, Items.bottomless_bucket]
                if RAKE:
                    templates.append(Items.rake)
                if MAGIC_SECATEURS:
                    templates.append(Items.magic_secateurs)

                equipment = find_by_templates(templates, 
                                              tab_iii, 
                                              bounds=play_area.bounds)
                for item in equipment:
                    click(item)
                
                enough_stock, coords_of_herb_seed = self.check_stock(tab_iii, Items.herb_seed)
                if enough_stock:
                    click(wait(template=Bank.quantity_5, bounds=play_area.bounds))
                    click(coords_of_herb_seed)

                # Tab all & quantity 1
                try:
                    click(wait(template=Bank.quantity_1, template_tol=0.6,
                            timeout=0.5))
                except:
                    log_event('Already on "Withdraw 1" in bank.')
                    pass
                click(find_by_template(screenshot=tab_iii,
                                       template_path=Bank.tab_all))
                tab_all = capture_runelite_window()
                templates = []
                if ardougne_cloak:
                    templates += [Armor.ardougne_cloak]
                if explorers_ring:
                    templates += [Items.explorers_ring]
                if templates:
                    equipment = find_by_templates(templates, tab_all, 
                                                bounds=play_area.bounds)
                    for item in equipment:
                        click(item)

                click(find_by_template(tab_all,
                                       Items.skills_necklace))

                # Quantity 10
                click(find_by_template(tab_all, Bank.quantity_10))

                enough_air_runes, air_runes = self.check_stock(tab_all, Runes.air)
                if enough_air_runes:
                    click(air_runes)
                    click(air_runes)

                enough_earth_runes, earth_runes = self.check_stock(tab_all, Runes.earth)
                if enough_earth_runes:
                    click(earth_runes)

                enough_law_runes, law_runes = self.check_stock(tab_all, Runes.law)
                if enough_law_runes:
                    click(law_runes)

                if not ardougne_cloak or not explorers_ring:
                    enough_water_runes, water_runes = self.check_stock(tab_all, Runes.water)
                    if enough_water_runes:
                        click(water_runes)
                        
                press('esc')

                if MAGIC_SECATEURS:
                    # Equip secateurs
                    screenshot = capture_runelite_window()
                    click(find_by_template(screenshot, Items.magic_secateurs))
                
                self.transition_state(FarmStates.GO_TO_NEXT_FARM)

            elif self.state == FarmStates.GO_TO_NEXT_FARM:
                if farm == 1:
                    self.transition_state(FarmStates.NAVIGATE_TO_HOSIDIUS)
                elif farm == 2:
                    self.transition_state(FarmStates.NAVIGATE_TO_CATHERBY)
                elif farm == 3:
                    self.transition_state(FarmStates.NAVIGATE_TO_FALADOR)
                elif farm == 4:
                    self.transition_state(FarmStates.NAVIGATE_TO_ARDOUGNE)
                elif farm == 5:
                    self.transition_state(FarmStates.NAVIGATE_TO_FARMING_GUILD)
            
            elif self.state == FarmStates.NAVIGATE_TO_HOSIDIUS:
                if not self.teleport_outside_house() or \
                      not self.walk_to_hosidius_patch():
                    self.transition_state(FarmStates.FAILED)
                self.transition_state(FarmStates.HARVEST_HERB)
            
            elif self.state == FarmStates.NAVIGATE_TO_CATHERBY:
                if not self.teleport_to_camelot() or \
                not self.walk_to_catherby_patch():
                    self.transition_state(FarmStates.FAILED)
                self.transition_state(FarmStates.HARVEST_HERB)

            elif self.state == FarmStates.NAVIGATE_TO_ARDOUGNE:
                if ardougne_cloak:
                    if not self.teleport_with_cloak() or \
                        not self.walk_to_ardougne_patch():
                        self.transition_state(FarmStates.FAILED)
                    self.transition_state(FarmStates.HARVEST_HERB)
                else:
                    if not self.teleport_to_ardougne() or \
                    not self.long_walk_to_ardougne_patch():
                        self.transition_state(FarmStates.FAILED)
                    self.transition_state(FarmStates.HARVEST_HERB)

            elif self.state == FarmStates.NAVIGATE_TO_FALADOR:
                if explorers_ring:
                    if not self.teleport_with_ring() or \
                            not self.walk_to_falador_patch():
                        self.transition_state(FarmStates.FAILED)
                    self.transition_state(FarmStates.HARVEST_HERB)
                else:
                    if not self.teleport_to_falador() or \
                    not self.long_walk_to_falador_patch():
                        self.transition_state(FarmStates.FAILED)
                    self.transition_state(FarmStates.HARVEST_HERB)

            elif self.state == FarmStates.NAVIGATE_TO_FARMING_GUILD:
                if not self.teleport_with_necklace() or \
                not self.walk_to_guild_patch():
                    self.transition_state(FarmStates.FAILED)
                self.transition_state(FarmStates.HARVEST_HERB)

            elif self.state == FarmStates.FAILED:
                press('esc')
                return False
                
            elif self.state == FarmStates.HARVEST_HERB:
                if wait(self.herb_tile, bounds=play_area.bounds):
                    if not click(wait(self.herb_tile, bounds=play_area.bounds)):
                        self.transition_state(FarmStates.FAILED)
                    self.transition_state(FarmStates.HARVESTING)
                    continue
                else:
                    pass

            elif self.state == FarmStates.HARVESTING:
                herb_patch_exhausted = self.harvesting()
                self.transition_state(FarmStates.CLEAN_HERBS)
            
            elif self.state == FarmStates.CLEAN_HERBS:
                ready_for_notes = self.clean_herbs() # True or False
                if ready_for_notes:
                    self.transition_state(FarmStates.TURN_INTO_NOTES)
                else:
                    self.transition_state(FarmStates.PLANT_SEED)

            elif self.state == FarmStates.TURN_INTO_NOTES:
                screenshot = capture_runelite_window()
                clean_herb = find_by_color(self.clean_herb, screenshot, 
                                            bounds=inventory.bounds)
                tool_lep = find_by_color(self.tool_leprechaun, screenshot, 
                                            bounds=play_area.bounds)
                if not clean_herb or not tool_lep:
                    self.transition_state(FarmStates.FAILED)
                    continue
                else:
                    click(clean_herb)
                    click(tool_lep)
                    sleep(5)
                    press('space')
                if herb_patch_exhausted:
                    self.transition_state(FarmStates.PLANT_SEED)
                else:
                    self.transition_state(FarmStates.HARVEST_HERB)
            
            elif self.state == FarmStates.PLANT_SEED:
                empty_herb_patch = wait(self.empty_patch, bounds=play_area.bounds)
                if empty_herb_patch:
                    click(wait(self.herb_seed, bounds=inventory.bounds))
                    x, y = empty_herb_patch
                    position = x,y+50
                    click(position)
                    sleep(5)
                    
                    # Check that the seed actually got planted
                    empty_herb_patch = wait(self.empty_patch, bounds=play_area.bounds,
                                            timeout=1)
                    if empty_herb_patch:
                        click(empty_herb_patch)
                        sleep(7)
                        continue

                    self.transition_state(FarmStates.COMPOST)
                else:
                    self.transition_state(FarmStates.HARVEST_HERB)


            elif self.state == FarmStates.COMPOST:
                click(wait(self.bottomless_compost, bounds=inventory.bounds))
                click(wait(self.herb_tile, bounds=play_area.bounds))
                sleep(3)
                if farm == 5:
                    log_use("farm_run", overwrite=True)
                    self.transition_state(FarmStates.FINISH_AT_BANK)
                else:
                    farm += 1
                    self.transition_state(FarmStates.GO_TO_NEXT_FARM)

            elif self.state == FarmStates.FINISH_AT_BANK:
                bounds = minimap.bounds
                click(wait(Pathing.step_2, bounds=bounds))
                click(wait(Pathing.step_3, bounds=bounds))
                sleep(6)
                self.transition_state(FarmStates.SUCCESS)

            elif self.state == FarmStates.SUCCESS:
                return True