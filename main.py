import random

from config import (
    BIRDHOUSE_RUN, HERB_RUN, 
    MAHOGANY_TREES, FUNGUS, PICKPOCKET, POTIONS,
    START, END, DO_RUNS
)
from tasks.birdhouse_run import BirdhouseRun
from tasks.fungus import Fungus
from tasks.mahogany_logs import ChopMahoganyTrees
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


def sleep_until_bh():
    birdhouse_log = "utils/birdhouse_run"

    # Read and parse last run time
    with open(birdhouse_log, "r") as file:
        last_run_str = file.read().strip()
    last_run_time = datetime.strptime(last_run_str, "%m-%d-%Y %H:%M")

    # Convert to UTC assuming the timestamp is in UTC
    last_run_time = last_run_time.replace(tzinfo=None)

    # Get current UTC time
    now_utc = datetime.utcnow()

    # Calculate next run time: 50 min + 2 min buffer
    next_run_time = last_run_time + timedelta(minutes=52)
    time_to_wait = (next_run_time - now_utc).total_seconds()

    if time_to_wait > 0:
        print(f"[O] Sleeping for {time_to_wait:.2f} seconds until next birdhouse run.")
        logout_now()
        sleep(time_to_wait)
    else:
        print("[O] Birdhouse run is ready. No need to sleep.")

    return True


def is_bedtime():
    now = datetime.now().time()
    start = time(START, 0)
    end = time(END, 0)

    # Check if now is between 11 PM and 5 AM (overnight range)
    return now >= start or now <= end


def main():
    while True:
        log_use("activity.log", overwrite=True)
        
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
            herb_run = check_time("farm_run", 95)
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
            continue

        now = datetime.now(ZoneInfo(key="America/New_York"))
        now = now.strftime("%m-%d-%Y %I:%M %p")

        if herb_run:
            login()
            print(f"{now}: Doing a farm run")

            f = FarmRun()
            f.start()
            continue

        if is_bedtime():
            logout_now()
            sleep(10)
            continue

        task_registry = {}
        if MAHOGANY_TREES:
            task_registry["Chop Mahogany Trees"] = ChopMahoganyTrees
        if FUNGUS:
            task_registry["Fungus"] = Fungus
        if PICKPOCKET:
            task_registry["Pickpocket Master Farmer"] = Pickpocket
        if POTIONS:
            task_registry["Potions"] = MakePotion

        if task_registry:
            with open("utils\\last_task", "r") as file:
                last_task = file.read().strip()
            
            entries = []
            for entry in task_registry.values():
                entries.append(entry)
            
            if last_task:
                entries += [task_registry.get(last_task)] * 8
            
            choice = random.choice(entries)

            for name, cls in task_registry.items():
                if cls == choice:
                    print(f"{now}: Starting {name}")
                    with open("utils\\last_task", "w") as file:
                        file.write(name)
            
            task = choice()

            if not task.start():
                break
            


if __name__ == "__main__":
    main()