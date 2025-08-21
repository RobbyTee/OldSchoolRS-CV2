from enum import Enum, auto
from pyautogui import press
from runelite_library.area import whole, minimap, play_area
from runelite_library.bank import open_bank
from runelite_library.filters import wait, find_by_template, find_by_templates, find_by_color
from runelite_library.interaction import click, get_worn_equipment, right_click
from runelite_library.inventory import avg_color_in_last_inventory
from runelite_library.logger import log_event, log_state, read_prev_state
from runelite_library.window_management import capture_runelite_window
from time import sleep
from too_many_items import Bank, Global_Colors, Items, Menu, Misc, Pathing


class MahoganyStates(Enum):
    INIT = auto()
    DETERMINE_LOCATION = auto()
    DETERMINE_EQUIPMENT = auto()
    OPEN_BANK = auto()
    WITHDRAW_EQUIPMENT = auto()
    FAILED = auto()
    GO_TO_MAHOGANY_TREES = auto()
    TELEPORT_TO_FOSSIL_ISLAND = auto()
    TELEPORT_TO_MUSHROOM_MEADOW = auto()
    WALK_TO_TREES_FROM_BANK = auto()
    WALK_TO_TREES_FROM_MUSHTREE = auto()
    CHOP_TREES = auto()
    WALK_TO_BANK = auto()
    SUCCESS = auto()


class ChopMahoganyTrees:
    def start(self, start_state=MahoganyStates.INIT):
        state = start_state
        mushtree = (200, 30, 220)
        cave_exit = (80, 40, 160)
        cave_entrance = (200, 50, 180)
        mahogany_tree = (80, 255, 255)
        mahogany_logs = (150, 200, 50)

        while True:
            if state == MahoganyStates.INIT:
                log_event('Starting ChopMahoganyTrees in mahogany_logs.py.')
                # Initial stuff goes here
                state = MahoganyStates.DETERMINE_LOCATION
                log_state(state)

            elif state == MahoganyStates.DETERMINE_LOCATION:
                # If we are at the Fossil Island bank, just walk to the trees!
                fossil_island_bank = wait(template=Bank.fossil_island,
                                        timeout=1)
                if fossil_island_bank:
                    log_event('Starting at the Fossil Island bank')
                    digsite_pendant = False
                else:
                    digsite_pendant = True
                state = MahoganyStates.DETERMINE_EQUIPMENT
                log_state(state)

            elif state == MahoganyStates.DETERMINE_EQUIPMENT:
                # If we have a Dragon Axe equipped, no need to deposit inventory.
                try:
                    worn_equipment = get_worn_equipment()
                    keep_equipment = False
                    if worn_equipment:
                        for item in worn_equipment:
                            if item['id'] == 6739: # Dragon Axe
                                log_event('Already have a Dragon Axe equipped.')
                                keep_equipment = True
                    state = MahoganyStates.OPEN_BANK
                    log_state(state)
                except Exception as e:
                    print(e)
                    break

            elif state == MahoganyStates.OPEN_BANK:
                # Open bank up and deposit equipment and inventory as necessary
                if not open_bank():
                    state = MahoganyStates.FAILED
                    log_state(state)
                    continue

                templates = [Bank.deposit_inventory]

                if not keep_equipment:
                    templates += [Bank.deposit_equipment]

                screenshot = capture_runelite_window()
                coords = find_by_templates(templates, screenshot, 
                                            bounds=whole.bounds)
                
                for coord in coords:
                    click(coord)

                if digsite_pendant or not keep_equipment:
                    state = MahoganyStates.WITHDRAW_EQUIPMENT
                    log_state(state)
                    continue
                else:
                    press('esc')
                    state = MahoganyStates.GO_TO_MAHOGANY_TREES
                    log_state(state)
                    continue

            elif state == MahoganyStates.WITHDRAW_EQUIPMENT:
                # Open tab III and withdraw a dragon axe.
                click(wait(template=Bank.tab_iii))
                screenshot = capture_runelite_window()

                if not keep_equipment:
                    click(find_by_template(screenshot, Items.dragon_axe))
                if digsite_pendant:
                    click(find_by_template(screenshot, Items.digsite_pendant))
                
                press('esc')
                if not keep_equipment:
                    click(wait(template=Items.dragon_axe)) # Equip it.
                state = MahoganyStates.GO_TO_MAHOGANY_TREES

            elif state == MahoganyStates.GO_TO_MAHOGANY_TREES:
                if digsite_pendant:
                    state = MahoganyStates.TELEPORT_TO_FOSSIL_ISLAND
                    log_state(state)
                else:
                    state = MahoganyStates.WALK_TO_TREES_FROM_BANK
                    log_state(state)

            elif state == MahoganyStates.TELEPORT_TO_FOSSIL_ISLAND:
                right_click(wait(template=Items.digsite_pendant))
                click(wait(template=Menu.rub))
                click(wait(template=Menu.fossil_island))
                state = MahoganyStates.TELEPORT_TO_MUSHROOM_MEADOW
                log_state(state)
                log_event("Teleported to Fossil Island")

            elif state == MahoganyStates.TELEPORT_TO_MUSHROOM_MEADOW:
                if click(wait(mushtree, timeout=3)):
                    click(wait(template=Menu.mushroom_meadow))
                    sleep(4)
                    log_event("Used Mushtree to teleport to Mushroom Meadow")
                    if wait(Pathing.step_10, bounds=minimap.bounds, timeout=3):
                        state = MahoganyStates.WALK_TO_TREES_FROM_MUSHTREE
                        log_state(state)
                else:
                    click(wait(Pathing.step_1, bounds=minimap.bounds))
                    sleep(3)

            elif state == MahoganyStates.WALK_TO_TREES_FROM_MUSHTREE:
                bounds = minimap.bounds
                click(wait(Pathing.step_1, bounds=bounds))
                click(wait(Pathing.step_2, bounds=bounds))
                click(wait(Pathing.step_3, bounds=bounds))
                click(wait(Pathing.step_10, bounds=bounds))
                click(wait(Pathing.step_9, bounds=bounds))
                click(wait(Pathing.step_8, bounds=bounds))
                state = MahoganyStates.CHOP_TREES
                log_state(state)

            elif state == MahoganyStates.WALK_TO_TREES_FROM_BANK:
                bounds = minimap.bounds
                click(wait(Pathing.step_6, bounds=bounds))
                click(wait(Pathing.step_5, bounds=bounds))
                sleep(5)
                click(wait(cave_entrance))
                sleep(5)
                state = MahoganyStates.CHOP_TREES
                log_state(state)

            elif state == MahoganyStates.CHOP_TREES:
                screenshot = capture_runelite_window()

                if avg_color_in_last_inventory(screenshot) != Global_Colors.last_inv:
                    state = MahoganyStates.WALK_TO_BANK
                    log_state(state)
                    continue

                if not find_by_template(screenshot, Misc.woodcutting):
                    screenshot = capture_runelite_window()
                    tree = find_by_color(mahogany_tree, screenshot, bounds=play_area.bounds)
                    if not tree:
                        click(wait(Pathing.step_8, bounds=minimap.bounds))
                        sleep(4)
                    else:
                        click(tree)
                        sleep(4)

            elif state == MahoganyStates.WALK_TO_BANK:
                bounds = minimap.bounds
                click(wait(Pathing.step_7, bounds=bounds))
                sleep(5)
                click(wait(cave_exit))
                sleep(5)
                click(wait(Pathing.step_5, bounds=bounds))
                click(wait(Pathing.step_6, bounds=bounds))
                click(wait(Pathing.step_7, bounds=bounds))
                sleep(5)
                state = MahoganyStates.SUCCESS
                log_state(state)

            elif state == MahoganyStates.SUCCESS:
                log_event("Completed a full inventory of Mahogany logs.")
                return True

            elif state == MahoganyStates.FAILED:
                prev_state = read_prev_state()
                log_event(f"Failed on: {prev_state}")
                return False