import random

from config import (
    BIRDHOUSE_RUN, HERB_RUN, 
    MAHOGANY_TREES, FUNGUS, PICKPOCKET, 
    UNFINISHED_POTIONS, POTIONS, DUPLICATE,
    START, END, DO_RUNS
)
from tasks.birdhouse_run import BirdhouseRun
from tasks.fungus import Fungus
from tasks.mahogany_logs import ChopMahoganyTrees
from tasks.make_unf_potions import MakeUnfPotion
from tasks.make_potions import MakePotion
from tasks.master_farmer import Pickpocket
from tasks.farm_run import FarmRun
from runelite_library.check_charges import log_use
from runelite_library.window_management import activate_app
from runelite_library.check_charges import check_time
from runelite_library.login import login, logout_now
from time import sleep
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo


def is_bedtime():
    now = datetime.now().time()
    start = time(START, 0)
    end = time(END, 0)

    # Check if now is between 11 PM and 5 AM (overnight range)
    return now >= start or now <= end


def main():
    log_use("activity.log", overwrite=True)
    while True:
        activate_app('runelite')

        if not DO_RUNS:
            if is_bedtime():
                logout_now()
                sleep(10)
                continue

        # Check recurring tasks
        if BIRDHOUSE_RUN:
            bh_run = check_time("birdhouse_run", 52)
        else:
            bh_run = False

        if HERB_RUN:
            herb_run = check_time("farm_run", 82)
        else:
            herb_run = False

        now = datetime.now(ZoneInfo(key="America/New_York"))
        now = now.strftime("%m-%d-%Y %I:%M %p")

        if bh_run:
            login()
            print(f"{now}: Doing a birdhouse run")

            b = BirdhouseRun()
            if not b.start():
                log_use("birdhouse_run", overwrite=True)
                print("   Failed this birdhouse run!")
                return False

        now = datetime.now(ZoneInfo(key="America/New_York"))
        now = now.strftime("%m-%d-%Y %I:%M %p")

        if herb_run:
            login()
            print(f"{now}: Doing a farm run")

            f = FarmRun()
            if not f.start():
                log_use("farm_run", overwrite=True)
                print("    Failed this farm run.")
                return False

        if is_bedtime():
            sleep(200)
            logout_now()
            continue

        task_registry = {}
        if MAHOGANY_TREES:
            task_registry["Chop Mahogany Trees"] = ChopMahoganyTrees
        if FUNGUS:
            task_registry["Fungus"] = Fungus
        if PICKPOCKET:
            task_registry["Pickpocket Master Farmer"] = Pickpocket
        if UNFINISHED_POTIONS:
            task_registry["Unfinished Potions"] = MakeUnfPotion
        if POTIONS:
            task_registry["Make Potions"] = MakePotion

        if task_registry:
            login()
            with open("utils\\last_task", "r") as file:
                last_task = file.read().strip()
            
            entries = []
            for entry in task_registry.values():
                entries.append(entry)
            
            if last_task:
                if last_task in task_registry.keys():
                    entries += [task_registry.get(last_task)] * DUPLICATE
                else:
                    pass
            
            choice = random.choice(entries)

            for name, cls in task_registry.items():
                if cls == choice:
                    print(f"{now}: Starting {name}")
                    with open("utils\\last_task", "w") as file:
                        file.write(name)
            
            task = choice()

            if not task.start():
                break
            continue
            
        sleep(15)

if __name__ == "__main__":
    main()