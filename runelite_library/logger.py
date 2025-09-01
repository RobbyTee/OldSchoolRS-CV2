import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if not exists
LOG_DIR = Path("utils")
LOG_DIR.mkdir(exist_ok=True)

# File paths
ACTIVITY_LOG_PATH = LOG_DIR / "activity.log"
STATE_LOG_PATH = LOG_DIR / "current_state.log"
PREV_STATE_LOG_PATH = LOG_DIR / "prev_state.log"

def setup_logger(name, log_file, level=logging.DEBUG, formatter=None):
    """Creates and returns a logger with rotation."""
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    if not formatter:
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(handler)

    logger.propagate = False
    return logger

# Activity logger for detailed troubleshooting
activity_logger = setup_logger("activity_logger", ACTIVITY_LOG_PATH)

# --- Public API ---

def log_event(message: str, level="info"):
    """Log a generic event to activity.log."""
    getattr(activity_logger, level.lower())(message)

def log_state(state):
    """Overwrite the current state to state.log for recovery purposes."""
    try:
        with open(STATE_LOG_PATH, "r") as f:
            current_state = f.read()
        with open(PREV_STATE_LOG_PATH, "w") as f:
            f.write(current_state)
    except FileNotFoundError:
        pass
    
    with open(STATE_LOG_PATH, "w") as f:
        f.write(str(state))

def read_state():
    """Read the last known state from state.log."""
    try:
        with open(STATE_LOG_PATH, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def read_prev_state():
    """Read the last known state from state.log."""
    try:
        with open(PREV_STATE_LOG_PATH, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None