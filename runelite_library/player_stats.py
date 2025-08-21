import numpy as np
from runelite_library.window_management import get_active_window_bounds
from runelite_library.area import health


def current_health(screenshot, window_origin=None, debug=False):
    """
    Calculates the average color of the health bar region.

    Args:
        screenshot (np.ndarray): Full RGB or RGBA screenshot of the Runelite window.
        window_origin (tuple): (x1, y1) top-left corner of the window.
        debug (bool): If True, saves the cropped health region for inspection.

    Returns:
        tuple: Average (R, G, B) color as integers.
    """
    if window_origin is None:
        x1, y1 = get_active_window_bounds()[:2]
    else:
        x1, y1 = window_origin

    bounds = health.bounds
    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    cropped = screenshot[screenshot_top:screenshot_top + h,
                         screenshot_left:screenshot_left + w]

    if debug:
        import cv2
        cv2.imwrite("debug_health_region.png", cropped)

    if cropped.shape[2] == 4:
        cropped = cropped[:, :, :3]  # Remove alpha channel

    avg_color = np.mean(cropped.reshape(-1, 3), axis=0)
    return tuple(int(round(c)) for c in avg_color)