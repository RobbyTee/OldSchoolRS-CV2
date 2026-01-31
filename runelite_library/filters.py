import cv2
import io
import numpy as np
import random
import requests

from runelite_library.logger import log_event
from runelite_library.window_management import (
    get_active_window_bounds, capture_runelite_window)
from runelite_library.area import play_area, whole
from scipy.ndimage import label, center_of_mass, binary_dilation, find_objects
from time import sleep, time


def find_by_color(rgb_color, screenshot, tolerance=0, 
                  bounds=None, window_origin=None, debug=False):
    if bounds is None:
        bounds = whole.bounds
        
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    
    x1, y1 = window_origin
    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    cropped = screenshot[screenshot_top:screenshot_top + h,
                        screenshot_left:screenshot_left + w]

    if debug:
        cv2.imwrite("debug.png", cropped)

    img_bgr = cv2.cvtColor(cropped[:, :, :3], cv2.COLOR_RGB2BGR)

    lower = np.clip(np.array(rgb_color) - tolerance, 0, 255)
    upper = np.clip(np.array(rgb_color) + tolerance, 0, 255)

    mask = cv2.inRange(img_bgr, lower, upper)
    labeled_array, num_features = label(mask)

    if num_features == 0:
        return None

    centers = center_of_mass(mask, labeled_array, range(1, num_features + 1))
    y_center, x_center = centers[0]

    return int(x_center + x), int(y_center + y)


def find_by_template(screenshot, template_path, tolerance=0.6, debug=False):
    """
    Find a template in the RGB screenshot (captured via capture_runelite_window),
    and return its absolute screen coordinates.
    """
    x1, y1 = get_active_window_bounds()[:2]  # Screenshot origin

    # Ensure screenshot is RGB and strip alpha if needed
    if screenshot.shape[2] == 4:
        screenshot = screenshot[:, :, :3]

    # Load the template and convert to RGB
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found at {template_path}")
    #template_rgb = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    th, tw = template.shape[:2]

    # Match in RGB space
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if debug:
        debug_img = screenshot.copy()
        cv2.rectangle(debug_img, max_loc, (max_loc[0]+tw, max_loc[1]+th), (0, 255, 0), 2)
        cv2.imwrite("template_match_debug.png", debug_img)
        print(f"Match confidence: {max_val:.2f}")

    if max_val >= tolerance:
        center_x = max_loc[0] + tw // 2 + x1
        center_y = max_loc[1] + th // 2 + y1
        return center_x, center_y

    return None



def wait(rgb_color=None, template=None, templates=None, timeout=10, 
         interval=0.1, bounds=None, rgb_tol=0, template_tol=0.7, debug=False):
    if not bounds:
        bounds = whole.bounds

    start_time = time()
    if rgb_color:
        while time() - start_time < timeout:
            screenshot = capture_runelite_window()
            coords = find_by_color(rgb_color, screenshot=screenshot, 
                                   tolerance=rgb_tol, bounds=bounds,
                                   debug=debug)
            if coords:
                return coords
            sleep(interval)
        log_event(f"Could not click on color: {rgb_color}", "warning")
        return None
    elif template:
        while time() - start_time < timeout:
            screenshot = capture_runelite_window()
            coords = find_by_template(template_path=template,
                                      screenshot=screenshot, 
                                      tolerance=template_tol,
                                      debug=debug)
            if coords:
                return coords
            sleep(interval)
        log_event(f"Could not click on template: {template}", "warning")
        return None
    elif templates:
        while time() - start_time < timeout:
            screenshot = capture_runelite_window()
            coords = find_by_templates(template_paths=templates, bounds=bounds,
                                       screenshot=screenshot, debug=debug)
            if coords:
                return coords
            sleep(interval)
        return None


def count_by_color(rgb_color, screenshot, bounds, tolerance=0, window_origin=None, debug=False):
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin

    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    # Crop to bounds
    cropped = screenshot[screenshot_top:screenshot_top + h,
                         screenshot_left:screenshot_left + w]

    if debug:
        import cv2
        cv2.imwrite("debug_count_crop.png", cropped)

    # Convert to RGB if needed (from MSS format)
    img_rgb = cropped[:, :, :3]

    # Create mask for pixels within tolerance
    lower = np.clip(np.array(rgb_color) - tolerance, 0, 255)
    upper = np.clip(np.array(rgb_color) + tolerance, 0, 255)
    mask = np.all((img_rgb >= lower) & (img_rgb <= upper), axis=-1)

    # Count blobs (connected regions)
    _, num_features = label(mask)
    return num_features


def query_rf(screenshot, bounds, window_origin=None, type=None, object=None):
    """
    Crop a region from the full screenshot and send it to Roboflow for object detection.
    
    Args:
        screenshot (np.ndarray): The full Runelite window screenshot.
        bounds (dict): A dict with keys top, left, width, height.
        window_origin (tuple): The (x1, y1) top-left corner of the window.
        type (str): "single" for single match, or None for full list.
        object (str): Class name to filter if using "single".
    
    Returns:
        list or tuple: All predictions, or (x, y) of the first matching object.
    """
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin

    x = bounds["left"] - x1
    y = bounds["top"] - y1
    w = bounds["width"]
    h = bounds["height"]

    cropped = screenshot[y:y+h, x:x+w]

    # Convert BGR to RGB for correct JPEG colors
    cropped_rgb = cv2.cvtColor(cropped[:, :, :3], cv2.COLOR_RGB2BGR)

    # Encode to JPEG in-memory
    success, jpeg_bytes = cv2.imencode('.jpg', cropped_rgb)
    if not success:
        raise RuntimeError("Failed to encode image as JPEG")
    img_bytes = io.BytesIO(jpeg_bytes.tobytes())

    url = 'https://detect.roboflow.com/my-first-project-mlr3z/5?api_key=hrA9KD1EnjJMRRZHWNHl'

    response = requests.post(url, files={'file': ('screenshot.jpg', img_bytes, 'image/jpeg')})
    predictions = response.json().get('predictions', [])

    if not type:
        return predictions

    if type == "single":
        for this in predictions:
            if this['class'] == object:
                x = this['x']
                y = this['y'] + 20  # vertical offset tweak
                return int(x + bounds["left"]), int(y + bounds["top"])

    return None
            

def find_by_cic(inner_color, outer_color, screenshot, 
                bounds, window_origin=None, tolerance=3, debug=False):
    """
    Locate a composite shape defined by an inner and outer color (e.g., for UI elements).

    Args:
        inner_color (tuple): RGB color tuple for the inner region.
        outer_color (tuple): RGB color tuple for the surrounding region.
        screenshot (np.ndarray): Full Runelite window screenshot (RGB).
        bounds (dict): Cropping bounds: {'top', 'left', 'width', 'height'}
        window_origin (tuple): (x1, y1) offset of the Runelite window.
        tolerance (int): Color match tolerance.
    
    Returns:
        tuple or None: (x, y) coordinates if found, else None.
    """
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin

    x = bounds["left"] - x1
    y = bounds["top"] - y1
    w = bounds["width"]
    h = bounds["height"]

    cropped = screenshot[y:y+h, x:x+w]

    img_bgr = cv2.cvtColor(cropped[:, :, :3], cv2.COLOR_RGB2BGR)

    # Define RGB tolerance masks
    def get_mask(color, tol):
        lower = np.clip(np.array(color) - tol, 0, 255)
        upper = np.clip(np.array(color) + tol, 0, 255)
        return np.all((img_bgr[:, :, :3] >= lower) & (img_bgr[:, :, :3] <= upper), axis=-1)

    inner_mask = get_mask(inner_color, tolerance)
    outer_mask = get_mask(outer_color, tolerance)
    expanded_outer_mask = binary_dilation(outer_mask, iterations=3)

    labeled_inner, num_inner = label(inner_mask)

    for i in range(1, num_inner + 1):
        region_mask = labeled_inner == i
        if np.any(expanded_outer_mask & region_mask):
            cy, cx = center_of_mass(region_mask)
            return int(cx + bounds["left"]), int(cy + bounds["top"])

    return None


def find_all_by_color(rgb_color, screenshot, bounds, tolerance=3, timeout=2, window_origin=None):
    """
    Finds all blobs of a given color within a region and returns their center positions.

    Args:
        rgb_color (tuple): RGB color to detect.
        screenshot (np.ndarray): Full RGB screenshot.
        bounds (dict): {'top', 'left', 'width', 'height'} region to search.
        tolerance (int): Color match tolerance.
        timeout (float): Max seconds to search before giving up.
        window_origin (tuple): (x1, y1) origin of the active window.

    Returns:
        List[Tuple[int, int]]: Absolute screen coordinates of matching centers.
    """
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin

    x = bounds["left"] - x1
    y = bounds["top"] - y1
    w = bounds["width"]
    h = bounds["height"]

    start_time = time()

    while True:
        if time() - start_time > timeout:
            return []

        cropped = screenshot[y:y+h, x:x+w]

        img_bgr = cv2.cvtColor(cropped[:, :, :3], cv2.COLOR_RGB2BGR)

        # Generate mask
        lower = np.clip(np.array(rgb_color) - tolerance, 0, 255)
        upper = np.clip(np.array(rgb_color) + tolerance, 0, 255)
        mask = np.all((img_bgr[:, :, :3] >= lower) & (img_bgr[:, :, :3] <= upper), axis=-1)

        if not np.any(mask):
            continue

        labeled_array, num_features = label(mask.astype(np.uint8))
        if num_features == 0:
            continue

        centers = center_of_mass(mask, labeled_array, range(1, num_features + 1))
        return [(int(xc + bounds["left"]), int(yc + bounds["top"])) for yc, xc in centers]


def area_by_color(rgb_color, screenshot, bounds, window_origin=None, tolerance=0):
    """
    Finds the bounding box of all regions matching a given color.

    Args:
        rgb_color (tuple): RGB color to detect.
        screenshot (np.ndarray): Full screenshot of Runelite window.
        bounds (dict): {'top', 'left', 'width', 'height'} region to search.
        window_origin (tuple): (x1, y1) offset of the Runelite window.
        tolerance (int): Optional color tolerance.

    Returns:
        dict or None: Bounding box in screen coords or None if not found.
    """
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin

    x = bounds["left"] - x1
    y = bounds["top"] - y1
    w = bounds["width"]
    h = bounds["height"]

    cropped = screenshot[y:y+h, x:x+w]

    # Use inRange to create mask
    lower = np.clip(np.array(rgb_color) - tolerance, 0, 255)
    upper = np.clip(np.array(rgb_color) + tolerance, 0, 255)
    mask = cv2.inRange(cropped[:, :, :3], lower, upper)

    labeled_array, num_features = label(mask)
    if num_features == 0:
        return None

    slices = find_objects(labeled_array)
    min_top = min(slc[0].start for slc in slices)
    max_bottom = max(slc[0].stop for slc in slices)
    min_left = min(slc[1].start for slc in slices)
    max_right = max(slc[1].stop for slc in slices)

    return {
        "top": bounds["top"] + min_top,
        "left": bounds["left"] + min_left,
        "width": max_right - (min_left + 25),
        "height": max_bottom - (min_top + 40)
    }


def find_by_templates(template_paths, screenshot, bounds, 
                      window_origin=None, tolerance=0.6, debug=False):
    if window_origin is None:
        window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin

    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    # Crop screenshot to bounds
    cropped = screenshot[screenshot_top:screenshot_top + h, screenshot_left:screenshot_left + w]

    if debug:
        cv2.imwrite("debug_template_crop.png", cropped)

    # Convert screenshot to BGR (if RGB from mss)
    if cropped.shape[2] == 4:
        cropped = cropped[:, :, :3]
    screenshot_bgr = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)

    found_positions = []

    for template_path in template_paths:
        template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
        if template is None:
            print(f"[WARN] Template not found: {template_path}")
            continue

        th, tw = template.shape[:2]

        for scale in [0.97, 1.0, 1.03]:
            resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            rh, rw = resized_template.shape[:2]

            if screenshot_bgr.shape[0] < rh or screenshot_bgr.shape[1] < rw:
                continue

            result = cv2.matchTemplate(screenshot_bgr, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= tolerance:
                center_x = max_loc[0] + rw // 2 + x
                center_y = max_loc[1] + rh // 2 + y
                found_positions.append((center_x, center_y))
                break  # Stop trying other scales after first match

    return found_positions


def coordinate_in_area(bounds, screenshot=None , debug=False):
    window_origin = get_active_window_bounds()[:2]
    
    x1, y1 = window_origin
    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    if debug:
        cropped = screenshot[screenshot_top:screenshot_top + h,
                        screenshot_left:screenshot_left + w]
        cv2.imwrite("debug.png", cropped)

    rand_x = random.randint(0, w - 1)
    rand_y = random.randint(0, h - 1)

    # Translate it back to absolute screen coordinates
    absolute_x = x + rand_x
    absolute_y = y + rand_y

    return (absolute_x, absolute_y)


def find_all_by_template(screenshot, template_path, tolerance=0.6, debug=False, bounds=None):
    x1, y1 = get_active_window_bounds()[:2]

    # Strip alpha if needed
    if screenshot.shape[2] == 4:
        screenshot = screenshot[:, :, :3]

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found at {template_path}")

    if bounds is None:
        bounds = whole.bounds

    window_origin = get_active_window_bounds()[:2]
    x1, y1 = window_origin
    x, y, w, h = bounds["left"], bounds["top"], bounds["width"], bounds["height"]
    screenshot_left = x - x1
    screenshot_top = y - y1

    cropped = screenshot[screenshot_top:screenshot_top + h,
                        screenshot_left:screenshot_left + w]

    th, tw = template.shape[:2]

    result = cv2.matchTemplate(cropped, template, cv2.TM_CCOEFF_NORMED)

    # Get all locations above the threshold
    ys, xs = np.where(result >= tolerance)

    matches = []
    for (x, y) in zip(xs, ys):
        center_x = x + tw // 2 + x1
        center_y = y + th // 2 + y1
        matches.append((int(center_x), int(center_y)))

    if debug:
        debug_img = screenshot.copy()
        for (x, y) in zip(xs, ys):
            cv2.rectangle(
                debug_img,
                (x, y),
                (x + tw, y + th),
                (0, 255, 0),
                2
            )
        cv2.imwrite("template_match_debug_all.png", debug_img)
        print(f"Found {len(matches)} matches")

    return matches
