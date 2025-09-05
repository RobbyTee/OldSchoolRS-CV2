import random

from enum import Enum, auto
from datetime import datetime, time
from pyautogui import press
from time import sleep
from runelite_library.check_charges import log_use
from runelite_library.area import play_area, minimap
from runelite_library.interaction import click
from runelite_library.filters import wait
from runelite_library.logger import log_event, log_state
from runelite_library.login import login, logout_now
from too_many_items import Pathing


class AgilityStates(Enum):
    INIT = auto()
    CHECK_FOR_FAILURE = auto()
    CHECK_FOR_MARK = auto()
    CHECK_FOR_NEXT_OBSTACLE = auto()
    CHECK_FOR_BEDTIME = auto()
    CHECK_FOR_BREAK = auto()
    WALK_TO_START = auto()
    FAILED = auto()

class RooftopAgility:
    def __init__(self):
        self.bedtime = False
        self.state = None
        self.start_tile_color = (50, 250, 50)
        self.reset_tile_color = (0, 0, 0)
        self.agility_obstacle_color = (0, 255, 0)
        self.fail_tile = (200, 60, 30)
        self.mark_of_grace = (50, 200, 80)
        self.attempt = 0


    def transition(self, new_state):
        self.state = new_state
        log_state(self.state)


    def is_bedtime(self):
        now = datetime.now().time()
        start = time(23, 0)
        end = time(5, 0)
        return now >= start or now <= end


    def start(self):
        self.state = AgilityStates.INIT
        log_use("activity.log", overwrite=True)
        while True:

            if self.state == AgilityStates.INIT:
                login()
                self.transition(AgilityStates.CHECK_FOR_BEDTIME)

            elif self.state == AgilityStates.CHECK_FOR_BEDTIME:
                
                if self.is_bedtime():
                    self.bedtime = True
                    sleep(10)
                    continue
                elif self.bedtime:
                    self.bedtime = False
                    self.transition(AgilityStates.INIT)
                    continue
                else:
                    self.transition(AgilityStates.CHECK_FOR_BREAK)
                    continue
            
            elif self.state == AgilityStates.CHECK_FOR_BREAK:
                if int(random.uniform(0,300)) == 77:
                    sleep(int(random.uniform(30, 60)))
                    if int(random.uniform(0,3)) == 1:
                        press('u')
                    else:
                        press('i')    
                    sleep(10)
                    login()
                self.transition(AgilityStates.CHECK_FOR_FAILURE)


            elif self.state == AgilityStates.CHECK_FOR_FAILURE:
                if wait(self.fail_tile, timeout=0.5, bounds=play_area.bounds):
                    log_event("Oops, fell off the track!")
                    bounds = minimap.bounds
                    if not click(wait(Pathing.step_8, bounds=bounds, timeout=4, rgb_tol=15)):
                        print("Problem with step 8")
                    if not click(wait(Pathing.step_9, bounds=bounds, timeout=4, rgb_tol=15)):
                        print("Issue with step_9")
                    if not click(wait(Pathing.step_10, bounds=bounds, timeout=4, rgb_tol=15)):
                        print("Can't click step_10")
                    sleep(6)
                    if wait(self.start_tile_color, bounds=play_area.bounds):
                        log_event("Reset successfully.")
                        self.transition(AgilityStates.INIT)
                else:
                    self.transition(AgilityStates.CHECK_FOR_MARK)

            elif self.state == AgilityStates.CHECK_FOR_MARK:
                mark = wait(self.mark_of_grace, timeout=0.5)
                if click(mark):
                    sleep(4)
                    log_event("Picked up mark of grace!")
                self.transition(AgilityStates.CHECK_FOR_NEXT_OBSTACLE)
            
            elif self.state == AgilityStates.CHECK_FOR_NEXT_OBSTACLE:
                obstacle = wait(self.agility_obstacle_color, timeout=5, debug=True, bounds=play_area.bounds)
                if not obstacle:
                    self.transition(AgilityStates.FAILED)
                    continue
                else:
                    click(obstacle)
                    self.attempt = 0
                    sleep(7)
                    self.transition(AgilityStates.INIT)

            elif self.state == AgilityStates.FAILED:
                self.attempt += 1
                if self.attempt > 9:
                    return False
                else:
                    self.transition(AgilityStates.INIT)



        