from enum import Enum, auto
from pyautogui import press
from runelite_library.area import logout
from runelite_library.window_management import capture_runelite_window
from runelite_library.filters import wait, find_by_color, coordinate_in_area
from runelite_library.interaction import click, click_template
from runelite_library.logger import log_event, log_state
from time import sleep
from too_many_items import Login, Interfaces, Player


class LoginState(Enum):
    CHECK_LOGGED_IN = auto()
    CLICK_PLAY_NOW = auto()
    CLICK_TO_PLAY = auto()
    HANDLE_TRY_AGAIN = auto()
    HANDLE_OK = auto()
    LOGIN_SUCCESS = auto()
    LOGIN_FAILED = auto()


def login(start_state=LoginState.CHECK_LOGGED_IN):
    state = start_state
    log_state(state)

    while True:
        if state == LoginState.CHECK_LOGGED_IN:
            screenshot = capture_runelite_window()
            if find_by_color(screenshot=screenshot,
                                rgb_color=Player.player_tile):
                log_event("Already logged in.")
                log_state("LOGIN_SUCCESS")
                return True
            state = LoginState.CLICK_PLAY_NOW
            log_state("CLICK_PLAY_NOW")

        elif state == LoginState.CLICK_PLAY_NOW:
            screenshot = capture_runelite_window()
            if click_template(screenshot=screenshot,
                              template=Login.play_now_button):
                state = LoginState.CLICK_TO_PLAY
                log_state("CLICK_TO_PLAY")
            else:
                state = LoginState.HANDLE_TRY_AGAIN
                log_state("HANDLE_TRY_AGAIN")
        
        elif state == LoginState.CLICK_TO_PLAY:
            screenshot = capture_runelite_window()
            click_to_play = wait(template=Login.click_to_play_button)
            if click_to_play:
                click(click_to_play)
                sleep(4)
                log_event("Successfully logged in!")
                log_state("LOGIN_SUCCESS")
                return True
            else:
                state = LoginState.LOGIN_FAILED

        elif state == LoginState.HANDLE_TRY_AGAIN:
            screenshot = capture_runelite_window()
            if click_template(screenshot=screenshot,
                              template=Login.try_again):
                state = LoginState.CHECK_LOGGED_IN
                log_state("CHECK_LOGGED_IN")
            else:
                state = LoginState.HANDLE_OK
                log_state("HANDLE_OK")
        
        elif state == LoginState.HANDLE_OK:
            screenshot = capture_runelite_window()
            if click_template(screenshot=screenshot,
                              template=Login.ok):
                state = LoginState.CHECK_LOGGED_IN
                log_state("CHECK_LOGGED_IN")
            else:
                state = LoginState.LOGIN_FAILED
        
        elif state == LoginState.LOGIN_FAILED:
            log_event("Failed to login!", level="error")
            print("FAILED TO LOG IN")
            return False
        

def logout_now():
    press(Interfaces.logout_icon)
    try:
        click(coordinate_in_area(logout.bounds))
        return True
    except:
        return False