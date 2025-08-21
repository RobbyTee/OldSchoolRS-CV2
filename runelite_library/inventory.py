import numpy as np
import cv2
from runelite_library.window_management import get_active_window_bounds
from runelite_library.area import last_inv_spot

"""
Use this like:
if avg_color_in_last_inventory(variables) != tmi.Global_Colors.last_inv:
    inventory_full = True
"""

def avg_color_in_last_inventory(screenshot, window_origin=None, debug=False):
    """
    Computes the average RGB color of the last inventory slot.

    Args:
        screenshot (np.ndarray): Full screenshot of Runelite window.
        window_origin (tuple): (x1, y1) top-left corner of the Runelite window.
        debug (bool): If True, saves cropped region for visual inspection.

    Returns:
        tuple: Average (R, G, B) color as integers.
    """
    if window_origin is None:
        x1, y1 = get_active_window_bounds()[:2]
    else:
        x1, y1 = window_origin

    bounds = last_inv_spot.bounds
    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    cropped = screenshot[screenshot_top:screenshot_top + h,
                         screenshot_left:screenshot_left + w]

    if debug:
        cv2.imwrite("debug_last_inventory_slot.png", cropped)

    if cropped.shape[2] == 4:
        cropped = cropped[:, :, :3]  # Drop alpha if present

    avg_color = np.mean(cropped.reshape(-1, 3), axis=0)
    return tuple(int(round(c)) for c in avg_color)