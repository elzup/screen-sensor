import pyautogui
import time
import os 
from pathlib import Path
import cv2
import numpy as np


files = [
    "C:/Users/guild/OneDrive/Videos/Captures/click-target-m.png",
    "C:/Users/guild/OneDrive/Videos/Captures/click-target-b.png",
#    "C:/Users/guild/OneDrive/Videos/Captures/click-target-p.png"
]



path_fix = lambda f: str(Path(f))
files = list(map(path_fix, files))

def locale_on_screen(target_paths):
    # スクリーンショットを取得
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)  # PILからnumpy配列に変換


    if len(screenshot.shape) == 3:  # RGBの場合
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    else:  # すでにグレースケールの場合
        screenshot_gray = screenshot

    # 比較画像を読み込む
    for target_path in target_paths:
        template = cv2.imread(target_path, cv2.IMREAD_UNCHANGED)

        # テンプレートがRGBAの場合、グレースケールに変換
        if template.shape[2] == 4:  # RGBAの場合
            template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
        elif len(template.shape) == 3:  # RGBの場合
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    
        # テンプレートマッチング
        result = cv2.matchTemplate(screenshot_gray , template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.6:
            return max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2
    return None




screenshot = pyautogui.screenshot("current_screen.png")
print("Screenshot saved as current_screen.png")


if any(map(lambda f: not os.path.exists(f), files)):
    print("File not found:", files)
    os.exit()

while True:
    # location = pyautogui.locateOnScreen(str(file_mon), confidence=0.8)
    location = locale_on_screen(files)
    if location is not None:
        pyautogui.click(location)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    time.sleep(10)


