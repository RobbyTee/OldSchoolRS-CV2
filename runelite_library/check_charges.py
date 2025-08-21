
from datetime import datetime, timezone, timedelta


def get_current_utc_date():
    return datetime.now(timezone.utc)


def open_log(item):
    try:
        with open(f"utils/{item}", "r") as file:
            log = file.readlines()
    except FileNotFoundError:
        with open(f"utils/{item}", "w") as file:
            file.write("")
        return open_log(item)
    return log


def read_log(log, item):
    if not log:
        return 999

    try:
        last_entry_str = log[-1].strip()
        last_entry_time = datetime.strptime(last_entry_str, "%m-%d-%Y %H:%M").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)

        if now.date() > last_entry_time.date():
            # It's a new UTC day; reset the log
            with open(f"utils/{item}", "w") as file:
                file.write("")
            return 0
        else:
            return len(log)

    except Exception as e:
        return 999


def log_use(item, overwrite=None):
    try:
        now = datetime.now(timezone.utc)
        timestamp_str = now.strftime("%m-%d-%Y %H:%M")
        write_or_append = "a"
        
        if overwrite:
            write_or_append = "w"

        with open(f"utils/{item}", write_or_append) as file:
            file.write(f"{timestamp_str}\n")
        return True
    except:
        return False


def check_charges(item) -> int:
    log = open_log(item)

    if len(log) > 0:
        charges_used = read_log(log, item)
        return charges_used
    else:
        return 0
    

def check_time(item, minutes) -> str:
    log = open_log(item)
    try:
        last_timestamp_str = log[0].strip()
    except IndexError:
        return True
    
    last_timestamp = datetime.strptime(last_timestamp_str,
                                            "%m-%d-%Y %H:%M")
    last_timestamp = last_timestamp.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if now > last_timestamp + timedelta(minutes=minutes):
        return True
    else:
        return False