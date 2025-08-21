import mss
import numpy as np
import win32gui
import win32con
import ctypes

from time import sleep


def activate_app(app_name):
    def enum_windows_callback(hwnd, wildcard):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if app_name.lower() in window_text.lower():
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                return False  # Stop enumeration
        return True

    win32gui.EnumWindows(lambda hwnd, _: enum_windows_callback(hwnd, app_name), None)
    sleep(.1)
    return True


def make_dpi_aware():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-monitor DPI aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def get_active_window_bounds():
    make_dpi_aware()
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        # Get client rect (relative to window)
        left, top, right, bottom = win32gui.GetClientRect(hwnd)

        # Convert to screen coordinates
        top_left = win32gui.ClientToScreen(hwnd, (left, top))
        bottom_right = win32gui.ClientToScreen(hwnd, (right, bottom))
        
        return (*top_left, *bottom_right)

    return None


def offset_area_to_absolute(relative_area, client_bounds):
    x_offset, y_offset = client_bounds[0], client_bounds[1]
    return [
        relative_area[0] + x_offset,
        relative_area[1] + y_offset,
        relative_area[2] + x_offset,
        relative_area[3] + y_offset
    ]


def capture_runelite_window(name=None):  
    x1, y1, x2, y2 = get_active_window_bounds()
    bounds = {
        "top": y1,
        "left": x1,
        "width": x2 - x1,
        "height": y2 - y1
    }

    with mss.mss() as sct:
        screenshot = sct.grab(bounds)
        img_np = np.array(screenshot)
        if name:
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=name)
        return img_np