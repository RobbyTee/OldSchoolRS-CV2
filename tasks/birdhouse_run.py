from config import LOGS, RABBITS_FOOT
from enum import Enum, auto
from pyautogui import press
from runelite_library.area import whole, minimap, inventory, play_area
from runelite_library.bank import open_bank
from runelite_library.check_charges import log_use
from runelite_library.filters import find_by_template, find_by_templates, wait
from runelite_library.interaction import click, right_click, use_rgb1_on_rgb2, use_rgb_on_template
from runelite_library.logger import log_event, log_state, read_prev_state
from runelite_library.window_management import capture_runelite_window
from time import sleep
from too_many_items import Pathing, Bank, Items, Menu, Objects

logs_list = {
    "logs": Items.logs,
    "oak": Items.oak_logs,
    "willow": Items.willow_logs,
    "yew": Items.yew_logs,
    "mahogany": Items.mahogany_logs,
    "magic": Items.magic_logs,
    "redwood": Items.redwood_logs,
}

LOGS = logs_list.get(LOGS)

class BirdhouseState(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    WITHDRAW_EQUIPMENT = auto()
    TELEPORT_TO_FOSSIL_ISLAND = auto()
    TELEPORT_TO_VALLEY = auto()
    TELEPORT_TO_MEADOW = auto()
    GO_TO_BIRDHOUSE_4 = auto()
    HARVEST_BIRDHOUSE_1 = auto()
    HARVEST_BIRDHOUSE_2 = auto()
    HARVEST_BIRDHOUSE_3 = auto()
    HARVEST_BIRDHOUSE_4 = auto()
    MAKE_BIRDHOUSE = auto()
    SET_BIRDHOUSE = auto()
    RETURN_TO_BANK = auto()
    SUCCESS = auto()
    FAILED = auto()


class BirdhouseRun:
    def start(self, start_state=BirdhouseState.INIT):
        state = start_state
        log_state(state)
        mushtree = (200, 30, 220)
        empty_bh = None
        last_birdhouse = None

        while True:
            if state == BirdhouseState.INIT:
                # Initial stuff can go here
                log_event("Starting a birdhouse run.")
                state = BirdhouseState.OPEN_BANK
                log_state(state)
            
            elif state == BirdhouseState.OPEN_BANK:
                # Open bank and empty inventory and equipment
                if open_bank():
                    templates = [Bank.deposit_equipment, Bank.deposit_inventory]
                    screenshot = capture_runelite_window()
                    coords = find_by_templates(templates, screenshot, 
                                               bounds=whole.bounds)
                    for coord in coords:
                        click(coord)
                    state = BirdhouseState.WITHDRAW_EQUIPMENT
                    log_state(state)
                else:
                    state = BirdhouseState.FAILED
                    log_state(state)

            elif state == BirdhouseState.WITHDRAW_EQUIPMENT:
                # Tab 3 & Quantity 1
                try:
                    click(wait(template=Bank.tab_iii))
                    try:
                        click(wait(template=Bank.quantity_1, template_tol=0.6,
                                timeout=0.5))
                    except:
                        log_event('Already on "Withdraw 1" in bank.')
                        pass
                    tab_iii = capture_runelite_window()
                    if not click(wait(template=LOGS, bounds=play_area.bounds)):
                        return False
                    if not click(wait(template=LOGS, bounds=play_area.bounds)):
                        return False
                    if not click(wait(template=LOGS, bounds=play_area.bounds)):
                        return False
                    if not click(wait(template=LOGS, bounds=play_area.bounds)):
                        return False
                    equipment = [Items.chisel, Items.hammer]
                    if RABBITS_FOOT:
                        equipment += [Items.rabbits_foot]
                    coords = find_by_templates(equipment, tab_iii, whole.bounds)
                    for item in coords:
                        click(item)
                    # find_by_templates() will not find the digsite pendant
                    if not click(wait(template=Items.digsite_pendant)):
                        return False
                    # Quantity 10 for 40 Hammerstone seeds
                    click(wait(template=Bank.quantity_10))
                    hammerstone_seeds = [Items.hammerstone_seeds] * 4
                    coords = find_by_templates(hammerstone_seeds, tab_iii, whole.bounds)
                    for item in coords:
                        click(item)
                    log_event("Withdrew all equipment for birdhouse run.")
                    press('esc')
                    if RABBITS_FOOT:
                        click(wait(template=Items.rabbits_foot))
                    state = BirdhouseState.TELEPORT_TO_FOSSIL_ISLAND
                    log_state(state)
                except:
                    state = BirdhouseState.FAILED
                    log_state(state)
            
            elif state == BirdhouseState.TELEPORT_TO_FOSSIL_ISLAND:
                right_click(wait(template=Items.digsite_pendant))
                click(wait(template=Menu.rub))
                click(wait(template=Menu.fossil_island))
                log_event("Used digsite pendant to teleport to Fossil Island")
                state = BirdhouseState.TELEPORT_TO_VALLEY
                log_state(state)
            
            elif state == BirdhouseState.TELEPORT_TO_VALLEY:
                if click(wait(mushtree, timeout=3)):
                    click(wait(template=Menu.verdant_valley))
                    log_event("Used Mushtree to teleport to Verdant Valley")
                    state = BirdhouseState.HARVEST_BIRDHOUSE_1
                    log_state(state)
                else:
                    click(wait(Pathing.step_1, bounds=minimap.bounds))
                    sleep(3)

            elif state == BirdhouseState.MAKE_BIRDHOUSE:
                clockwork = (80, 100, 200)
                log = (150, 180, 30)
                screenshot = capture_runelite_window()
                if not use_rgb1_on_rgb2(screenshot=screenshot, rgb1=clockwork, 
                                rgb2=log, bounds=inventory.bounds):
                    continue
                sleep(3)
                log_event("Created a birdhouse")
                last_birdhouse = read_prev_state()
                if last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_1":
                    empty_bh = Objects.bh1
                elif last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_2":
                    empty_bh = Objects.bh2
                elif last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_3":
                    empty_bh = Objects.bh3
                elif last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_4":
                    empty_bh = Objects.bh4
                else:
                    state = BirdhouseState.FAILED
                    log_state(state)
                    continue
                    
                state = BirdhouseState.SET_BIRDHOUSE
                log_state(state)

            elif state == BirdhouseState.SET_BIRDHOUSE:
                hammerstone_seeds = (75, 150, 10)
                screenshot = capture_runelite_window()
                click(find_by_template(screenshot=screenshot, template_path=empty_bh))
                sleep(3)
                if not use_rgb_on_template(screenshot, hammerstone_seeds, empty_bh):
                    state = BirdhouseState.FAILED
                    log_state(state)
                    continue
                sleep(3)
                if last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_1":
                    state = BirdhouseState.HARVEST_BIRDHOUSE_2
                    log_state(state)
                if last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_2":
                    state = BirdhouseState.TELEPORT_TO_MEADOW
                    log_state(state)
                if last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_3":
                    state = BirdhouseState.GO_TO_BIRDHOUSE_4
                    log_state(state)
                if last_birdhouse == "BirdhouseState.HARVEST_BIRDHOUSE_4":
                    log_use('birdhouse_run', overwrite=True)
                    log_event("Logged birdhouse run.")
                    state = BirdhouseState.RETURN_TO_BANK
                    log_state(state)

            elif state == BirdhouseState.HARVEST_BIRDHOUSE_1:
                ready_bh_1 = (53, 75, 200)
                click(wait(ready_bh_1))
                state = BirdhouseState.MAKE_BIRDHOUSE
                log_state(state)
                log_event("Harvested birdhouse #1.")

            elif state == BirdhouseState.HARVEST_BIRDHOUSE_2:
                ready_bh_2 = (85, 97, 170)
                click(wait(Pathing.step_1, bounds=minimap.bounds))
                sleep(6)
                click(wait(ready_bh_2))
                state = BirdhouseState.MAKE_BIRDHOUSE
                log_state(state)
                log_event("Harvested birdhouse #2.")

            elif state == BirdhouseState.RETURN_TO_BANK:
                bounds = minimap.bounds
                click(wait(Pathing.step_1, bounds=bounds))
                click(wait(Pathing.step_2, bounds=bounds))
                click(wait(Pathing.step_3, bounds=bounds))
                click(wait(Pathing.step_4, bounds=bounds))
                click(wait(Pathing.step_5, bounds=bounds))
                click(wait(Pathing.step_6, bounds=bounds))
                click(wait(Pathing.step_7, bounds=bounds))
                sleep(6)
                state = BirdhouseState.SUCCESS
                log_state(state)

            elif state == BirdhouseState.TELEPORT_TO_MEADOW:
                click(wait(Pathing.step_2, bounds=minimap.bounds))
                sleep(4)
                click(wait(mushtree))
                click(wait(template=Menu.mushroom_meadow))
                state = BirdhouseState.HARVEST_BIRDHOUSE_3
                log_state(state)

            elif state == BirdhouseState.HARVEST_BIRDHOUSE_3:
                ready_bh_3 = (85, 97, 170)
                click(wait(Pathing.step_10, bounds=minimap.bounds))
                sleep(7)
                if not click(wait(ready_bh_3)):
                    continue
                state = BirdhouseState.MAKE_BIRDHOUSE
                log_state(state)
                log_event("Harvested birdhouse #3.")

            elif state == BirdhouseState.GO_TO_BIRDHOUSE_4:
                bounds = minimap.bounds
                click(wait(Pathing.step_1, bounds=bounds))
                click(wait(Pathing.step_2, bounds=bounds))
                click(wait(Pathing.step_3, bounds=bounds))
                click(wait(Pathing.step_4, bounds=bounds))
                click(wait(Pathing.step_5, bounds=bounds))
                click(wait(Pathing.step_6, bounds=bounds))
                sleep(6)
                state = BirdhouseState.HARVEST_BIRDHOUSE_4
                log_state(state)
                

            elif state == BirdhouseState.HARVEST_BIRDHOUSE_4:
                ready_bh_4 = (85, 97, 170)
                click(wait(ready_bh_4))
                state = BirdhouseState.MAKE_BIRDHOUSE
                log_state(state)
                log_event("Harvested birdhouse #4.")

            elif state == BirdhouseState.FAILED:
                prev_state = read_prev_state()
                log_event(f"Failed on: {prev_state}")
                return False
        
            elif state == BirdhouseState.SUCCESS:
                log_event("Finished birdhouse run!")
                return True