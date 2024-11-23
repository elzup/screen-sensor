import pyautogui


def screenshot():
    return pyautogui.screenshot()


def click(location):
    pyautogui.click(location)
