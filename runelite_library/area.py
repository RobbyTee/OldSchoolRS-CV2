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
        "top": y2 - 300,
        "left": x2 - 260,
        "width": 220,
        "height": 265
    }

@with_bounds
def _play(x1, y1, x2, y2):
    return {
        "top": y1,
        "left": x1,
        "width": (x2 - x1) - 265,
        "height": (y2 - y1) - 25
    }

@with_bounds
def _minimap(x1, y1, x2, y2):
    return {
        "top": y1 + 25,
        "left": x2 - 165,
        "width": 100,
        "height": 115
    }

@with_bounds
def _compass(x1, y1, x2, y2):
    return {
        "top": y1 + 15,
        "left": x2 - 200,
        "width": 20,
        "height": 20
    }

@with_bounds
def _last_inv_spot(x1, y1, x2, y2):
    return {
        "top": y2 - 77,
        "left": x2 - 107,
        "width": 40,
        "height": 40
    }

@with_bounds
def _health_area(x1, y1, x2, y2):
    return {
        "top": y1 + 54,
        "left": x2 - 212,
        "width": 20,
        "height": 20
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
        "top": y2 - 126,
        "left": x2 - 233,
        "width": 80,
        "height": 12
    }

@with_bounds
def _minigame_teleport(x1, y1, x2, y2):
    return {
        "top": y2 - 52,
        "left": x2 - 120,
        "width": 50,
        "height": 12
    }

@with_bounds
def _logout(x1, y1, x2, y2):
    return {
        "top": y2 - 80,
        "left": x2 - 200,
        "width": 100,
        "height": 20
    }

@with_bounds
def _home_teleport(x1, y1, x2, y2):
    return {
        "top": y2 - 280,
        "left": x2 - 230,
        "width": 15,
        "height": 15
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