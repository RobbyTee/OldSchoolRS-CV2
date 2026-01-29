from config import BANK_PIN
from enum import Enum, auto
from pyautogui import press
from runelite_library.area import play_area
from runelite_library.filters import wait
from runelite_library.interaction import click
from runelite_library.logger import log_event, log_state
from runelite_library.recover import recover_to_bank
from too_many_items import Bank
from time import sleep

class BankStates(Enum):
    INIT = auto()
    CLICK_BANK = auto()
    ENTER_PIN = auto()
    VERIFY_OPEN_BANK = auto()
    SUCCESS = auto()
    FAILED = auto()
    RECOVER = auto()


def open_bank(start_state=BankStates.INIT):
    state = start_state
    log_state(state)

    while True:
        if state == BankStates.INIT:
            # Initial stuff here
            state = BankStates.CLICK_BANK
            log_state(state)        
        
        elif state == BankStates.CLICK_BANK:
            log_state(state)
            try:
                click(wait(rgb_color=Bank.bank,
                           bounds=play_area.bounds))
                state = BankStates.ENTER_PIN
                log_state(state)
            except:
                state = BankStates.RECOVER
        
        elif state == BankStates.ENTER_PIN:
            log_state(state)
            bank_pin = wait(template=Bank.bank_pin_screen,
                            timeout=2)
            if bank_pin:
                press(BANK_PIN[0])
                sleep(0.5)
                press(BANK_PIN[1])
                sleep(0.4)
                press(BANK_PIN[2])
                sleep(0.6)
                press(BANK_PIN[3])
                
            state = BankStates.VERIFY_OPEN_BANK

        elif state == BankStates.VERIFY_OPEN_BANK:
            log_state(state)
            open_bank = wait(template=Bank.deposit_inventory,
                             timeout=3)
            if open_bank:
                state = BankStates.SUCCESS
            else:
                state = BankStates.FAILED

        elif state == BankStates.SUCCESS:
            log_event("Bank opened successfully")
            return True

        elif state == BankStates.FAILED:
            log_state(state)
            log_event("Oops! Something went wrong.", level="warn")
            press('esc')
            state = BankStates.RECOVER

        elif state == BankStates.RECOVER:
            log_state(state)
            log_event("Attempting to recover to bank", level="warn")
            if recover_to_bank():
                state = BankStates.CLICK_BANK
            else:
                return False