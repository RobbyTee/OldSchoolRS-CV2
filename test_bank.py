from enum import Enum, auto
from pyautogui import press
from runelite_library.bank import open_bank
from runelite_library.filters import wait
from runelite_library.interaction import click
from runelite_library.logger import log_event
from runelite_library.window_management import activate_app
from too_many_items import Bank, Runes


class BankStates(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    TEST = auto()
    FAILED = auto()
    SUCCESS = auto()

def test_bank_interfaces():

    activate_app("runelite")

    state = BankStates.INIT
    while True:
        if state == BankStates.INIT:
            state = BankStates.OPEN_BANK
            continue

        elif state == BankStates.OPEN_BANK:
            log_event("Opening bank.")
            if open_bank():
                state = BankStates.TEST
                continue
            else:
                log_event("Failed to open bank.")
                state = BankStates.FAILED
                continue

        elif state == BankStates.TEST:
            bank_tabs = [
                Bank.tab_all, Bank.tab_i, Bank.tab_ii, Bank.tab_iii,
                Bank.tab_iv, Bank.tab_v, Bank.tab_vi, Bank.tab_vii, 
                Bank.tab_viii, Bank.tab_ix,

                Bank.deposit_equipment, Bank.deposit_inventory,
                Bank.quantity_x, Bank.quantity_10, Bank.quantity_5,
                Bank.quantity_all, Bank.quantity_1
                         ]
            
            for template in bank_tabs:
                try:
                    result = click(wait(template=template, timeout=0.5))
                    if result:
                        log_event(f"Found: {template}")
                    else:
                        log_event(f"Could not find: {template}", level="error")
                except:
                    state = BankStates.FAILED
                    continue
            
            state = BankStates.SUCCESS
            continue

        elif state == BankStates.FAILED:
            press('esc')
            print("Something failed. Check logs.")
            return 1

        elif state == BankStates.SUCCESS:
            press('esc')
            print("Completed testing bank interfaces! Check logs.")
            return 0


class RuneStates(Enum):
    INIT = auto()
    OPEN_BANK = auto()
    TEST = auto()
    SUCCESS = auto()
    FAILED = auto()


def test_runes():
    activate_app("runelite")
    state = RuneStates.INIT

    while True:
        if state == RuneStates.INIT:
            state = RuneStates.OPEN_BANK
            continue

        elif state == RuneStates.OPEN_BANK:
            log_event("Opening bank.")
            if open_bank():
                click(wait(template=Bank.tab_all))
                click(wait(template=Bank.deposit_inventory))
                state = RuneStates.TEST
                continue
            else:
                log_event("Failed to open bank.")
                state = RuneStates.FAILED
                continue

        elif state == RuneStates.TEST:
            rune_list = [
                Runes.air, Runes.blood, Runes.chaos, Runes.cosmic,
                Runes.death, Runes.earth, Runes.fire, Runes.law,
                Runes.mind
            ]
            
            for template in rune_list:
                try:
                    result = click(wait(template=template, timeout=0.5))
                    if result:
                        log_event(f"Found: {template}")
                    else:
                        log_event(f"Could not find: {template}", level="error")
                except:
                    state = RuneStates.FAILED
                    continue

            state = RuneStates.SUCCESS
            continue

        elif state == RuneStates.FAILED:
            press('esc')
            print("Something failed testing runes. Check logs.")
            return 1

        elif state == RuneStates.SUCCESS:
            press('esc')
            print("Completed testing runes! Check logs.")
            return 0


if __name__ == "__main__":
    bank_result = test_bank_interfaces()
    rune_result = test_runes()

    if any [
        bank_result,
        rune_result
    ] == 1:
        exit(1)
    else:
        exit(0)
