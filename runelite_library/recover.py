from enum import Enum, auto
from pyautogui import press
from runelite_library.area import \
    (fishing_trawler, minigame_teleport, home_teleport, minimap, play_area)
from runelite_library.check_charges import check_time, log_use
from runelite_library.filters import coordinate_in_area, wait
from runelite_library.interaction import click
from runelite_library.logger import log_event, log_state, read_prev_state
from time import sleep
from too_many_items import Interfaces, Menu, Bank, Pathing


class RecoverStates(Enum):
    INIT = auto()
    FISHING_TRAWLER = auto()
    HOME_TELEPORT = auto()
    NAVIGATE_TO_TRAPDOOR = auto()
    CLICK_TRAPDOOR = auto()
    NAVIGATE_TO_BANK = auto()
    SUCCESS = auto()
    FAILED = auto()


def teleport_to_fishing_trawler():
    press(Interfaces.minigame_icon) 
    click(wait(template=Menu.activity))
    sleep(0.1)
    click(coordinate_in_area(fishing_trawler.bounds))
    sleep(0.1)
    click(coordinate_in_area(minigame_teleport.bounds))
    press(Interfaces.inventory_icon)
    if wait(rgb_color=Bank.bank, timeout=20):
        log_use("minigame_teleport", overwrite=True)
        return True
    else:
        return False


def lumbridge_home_teleport():
    lumbridge_spawn = (255, 0, 144)
    press(Interfaces.spells_icon)
    click(coordinate_in_area(home_teleport.bounds))
    if wait(rgb_color=lumbridge_spawn, bounds=minimap.bounds, timeout=20):
        log_use("lumbridge_home_teleport", overwrite=True)
        return True
    else:
        return False


def navigate_to_trapdoor():
    click(wait(rgb_color=Pathing.step_1, bounds=minimap.bounds))
    sleep(12)
    trapdoor = (255, 0, 255)
    click(wait(trapdoor, bounds=play_area.bounds))
    click(wait(Bank.bank_floor, bounds=minimap.bounds))
    if wait(rgb_color=Bank.bank, timeout=20):
        print("Done")
        return True
    else:
        print("Failed")
        return False


def recover_to_bank(start_state=RecoverStates.INIT):
    state = start_state
    log_state(state)
    attempt_at_trapdoor = 0

    while True:
        if state == RecoverStates.INIT:
            # Initial stuff here
            state = RecoverStates.FISHING_TRAWLER

        elif state == RecoverStates.FISHING_TRAWLER:
            log_state(state)
            if check_time("minigame_teleport", 30): 
                if teleport_to_fishing_trawler():
                    state = RecoverStates.SUCCESS
                else:
                    state = RecoverStates.HOME_TELEPORT
            else:
                    state = RecoverStates.HOME_TELEPORT

        elif state == RecoverStates.HOME_TELEPORT:
            log_state(state)
            if check_time("lumbridge_home_teleport", 30):
                if lumbridge_home_teleport():
                    log_event("Teleported to Lumbridge via home teleport.")
                    state = RecoverStates.NAVIGATE_TO_TRAPDOOR
                else:
                    state = RecoverStates.FAILED
            else:
                state = RecoverStates.FAILED

        elif state == RecoverStates.NAVIGATE_TO_TRAPDOOR:
            log_state(state)
            press(Interfaces.inventory_icon)
            click(wait(Pathing.step_1, bounds=minimap.bounds))
            sleep(12)
            trapdoor = (255, 0, 255)
            if wait(trapdoor, bounds=play_area.bounds):
                state = RecoverStates.CLICK_TRAPDOOR
            else:
                state = RecoverStates.FAILED

        elif state == RecoverStates.CLICK_TRAPDOOR:
            log_state(state)
            trapdoor = (255, 0, 255)
            click(wait(trapdoor, bounds=play_area.bounds))
            bank_floor = wait(Bank.bank_floor, bounds=minimap.bounds)
            if bank_floor:
                click(bank_floor)
                sleep(8)
                state = RecoverStates.SUCCESS
            else:
                state = RecoverStates.FAILED

        elif state == RecoverStates.SUCCESS:
            log_event("Successfully recovered to bank.")
            return True

        elif state == RecoverStates.FAILED:
            log_state(state)
            if read_prev_state() == "RecoverStates.CLICK_TRAPDOOR":
                if attempt_at_trapdoor < 4:
                    attempt_at_trapdoor += 1
                    sleep(2)
                    state = RecoverStates.CLICK_TRAPDOOR
            else:
                log_event("Did not successfully recover to bank.", "error")
                return False