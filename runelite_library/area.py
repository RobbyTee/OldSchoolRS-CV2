from runelite_library.window_management import get_active_window_bounds


class Area:
    def __init__(self, bounds_func):
        self._bounds_func = bounds_func

    @property
    def bounds(self):
        return self._bounds_func()


def with_bounds(func):
    def wrapper():
        bounds = get_active_window_bounds()
        if not bounds:
            return None
        return func(*bounds)
    return wrapper

@with_bounds
def _inventory(x1, y1, x2, y2):
    return {
        "top": y2 - 670,
        "left": x2 - 532,
        "width": 455,
        "height": 660
    }

@with_bounds
def _play(x1, y1, x2, y2):
    return {
        "top": y1,
        "left": x1,
        "width": (x2 - x1) - 540,
        "height": (y2 - y1) - 50
    }

@with_bounds
def _minimap(x1, y1, x2, y2):
    return {
        "top": y1 + 50,
        "left": x2 - 325,
        "width": 195,
        "height": 225
    }

@with_bounds
def _compass(x1, y1, x2, y2):
    return {
        "top": y1 + 50,
        "left": x2 - 400,
        "width": 40,
        "height": 20
    }

@with_bounds
def _last_inv_spot(x1, y1, x2, y2):
    return {
        "top": y2 - 150,
        "left": x2 - 200,
        "width": 55,
        "height": 64
    }

@with_bounds
def _health_area(x1, y1, x2, y2):
    return {
        "top": y1 + 110,
        "left": x2 - 420,
        "width": 31,
        "height": 35
    }

@with_bounds
def _whole_window(x1, y1, x2, y2):
    return {
        "top": y1,
        "left": x1,
        "width": x2 - x1,
        "height": y2 - y1
    }

@with_bounds
def _fishing_trawler(x1, y1, x2, y2):
    return {
        "top": y2 - 255,
        "left": x2 - 465,
        "width": 190,
        "height": 25
    }

@with_bounds
def _minigame_teleport(x1, y1, x2, y2):
    return {
        "top": y2 - 110,
        "left": x2 - 250,
        "width": 100,
        "height": 25
    }

@with_bounds
def _logout(x1, y1, x2, y2):
    return {
        "top": y2 - 165,
        "left": x2 - 420,
        "width": 240,
        "height": 50
    }

@with_bounds
def _home_teleport(x1, y1, x2, y2):
    return {
        "top": y2 - 560,
        "left": x2 - 460,
        "width": 25,
        "height": 30
    }

@with_bounds
def _bank_window(x1, y1, x2, y2):
    return {
        "top": y2 - 415,
        "left": x1 + 40,
        "width": 950,
        "height": 80
    }


# --- Prewrapped Area objects (export these) ---

inventory = Area(_inventory)
play_area = Area(_play)
minimap = Area(_minimap)
compass = Area(_compass)
last_inv_spot = Area(_last_inv_spot)
health = Area(_health_area)
whole = Area(_whole_window)
fishing_trawler = Area(_fishing_trawler)
minigame_teleport = Area(_minigame_teleport)
logout = Area(_logout)
home_teleport = Area(_home_teleport)
bank_window = Area(_bank_window)