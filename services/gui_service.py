import pyautogui


def screenshot():
    try:
        ss = pyautogui.screenshot()
        return ss
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
    return None


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


def screen_size():
    return pyautogui.size()
