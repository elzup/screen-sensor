import pyautogui


def screenshot():
    return pyautogui.screenshot()


def click(location):
    pyautogui.click(location)


def mouseup():
    pyautogui.mouseUp()


def move(location):
    pyautogui.moveTo(location)


def click_back(location):
    prev_pos = pyautogui.position()
    mouseup()
    pyautogui.click(location)
    move(prev_pos)
