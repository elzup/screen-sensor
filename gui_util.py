import pyautogui


def screenshot():
    return pyautogui.screenshot()


def is_pressed():
    return pyautogui.mouseDown()


def click(location):
    pyautogui.click(location)


def move(location):
    pyautogui.moveTo(location)


def click_back(location):
    prev_pos = pyautogui.position()
    pyautogui.click(location)
    move(prev_pos)
