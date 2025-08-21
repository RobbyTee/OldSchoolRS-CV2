import pyautogui
import random
import requests
import json

from runelite_library.area import compass, play_area, whole, inventory
from runelite_library.filters import (
    find_by_template, find_by_color, find_all_by_color, 
    find_by_templates, find_by_cic, find_objects)
from runelite_library.logger import log_event
from time import sleep


def click(position):
    try:
        random_time = random.uniform(0.05, 0.3)
        x, y = position
        pyautogui.moveTo(x, y, duration=random_time, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        return True
    except TypeError:
        return False


def right_click(position):
    random_time = random.uniform(0.05, 0.3)
    x, y = position
    pyautogui.moveTo(x, y, duration=random_time, tween=pyautogui.easeInOutQuad)
    pyautogui.rightClick()
    return True


def click_no_move(position):
    x, y = position
    pyautogui.moveTo(x, y)
    pyautogui.click()
    return


def click_compass():
    bounds = compass()
    if not bounds:
        raise ValueError("Could not get compass bounds")

    x1 = bounds["left"]
    y1 = bounds["top"]
    width = bounds["width"]
    height = bounds["height"]

    # Click the center of the compass region
    center_x = x1 + width // 2
    center_y = y1 + height // 2

    pyautogui.moveTo(center_x, center_y, duration=0.2, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    return


def scroll_out():
    bounds = play_area()
    if not bounds:
        raise ValueError("Could not get play area bounds")

    x1 = bounds["left"]
    y1 = bounds["top"]
    width = bounds["width"]
    height = bounds["height"]

    # Random point within play area
    x = int(random.uniform(x1, x1 + width))
    y = int(random.uniform(y1, y1 + height))

    pyautogui.moveTo(x, y, duration=0.2, tween=pyautogui.easeInOutQuad)
    pyautogui.scroll(clicks=-4500)
    return


def pan_up():
    pyautogui.keyDown('up')
    sleep(4)
    pyautogui.keyUp('up')
    return


def get_worn_equipment() -> json:
    try:
        url = "http://127.0.0.1:8080/equip"
        response = requests.get(url)
        return response.json()
    except:
        return None
    

def click_template(screenshot, template) -> bool:
    coords = find_by_template(screenshot=screenshot,
                              template_path=template)
    if coords:
        click(coords)
        return True
    else:
        return False
    

def use_rgb1_on_rgb2(screenshot, rgb1, rgb2, bounds=None) -> bool:
    if bounds is None:
        bounds = whole.bounds
    try:
        rgb1_coords = find_by_color(rgb_color=rgb1, screenshot=screenshot,
                                      bounds=bounds)
        rgb2_coords = find_by_color(rgb_color=rgb2, screenshot=screenshot,
                            bounds=bounds)
        if rgb1_coords and rgb2_coords:
            click(rgb1_coords)
            click(rgb2_coords)
            return True
        else:
            return False
    except:
        return False


def use_rgb_on_template(screenshot, rgb, template, bounds=None) -> bool:
    if bounds is None:
        bounds = whole.bounds
    try:
        rgb_coords = find_by_color(rgb_color=rgb, screenshot=screenshot,
                            bounds=bounds)
        template_coords = find_by_template(template_path=template, screenshot=screenshot)
        if rgb_coords and template_coords:
            click(rgb_coords)
            click(template_coords)
            return True
        else:
            return False
    except Exception as e:
        return False


def use_template_on_rgb(screenshot, rgb, template, bounds=None) -> bool:
    if bounds is None:
        bounds = whole.bounds
    try:
        template_coords = find_by_template(template_path=template, screenshot=screenshot)
        rgb_coords = find_by_color(rgb_color=rgb, screenshot=screenshot,
                            bounds=bounds)
        if template_coords and rgb_coords:
            click(template_coords)
            click(rgb_coords)
            return True
        else:
            return False
    except:
        return False


def use_template1_on_template2(screenshot, template1, template2, bounds=None) -> bool:
    if bounds is None:
        bounds = whole.bounds
    
    try:
        template1_coords = find_by_template(template_path=template1, screenshot=screenshot)
        template2_coords = find_by_template(template_path=template2, screenshot=screenshot)
        if template1_coords and template2_coords:
            click(template1_coords)
            click(template2_coords)
            return True
        else:
            return False
    except:
        return False