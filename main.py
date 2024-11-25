import re
from typing import Union

from schemas import ScoutProfile
from services.gui_service import click_back, screenshot
from services.image_service import get_mats, locale_on_screen
from services.log_service import log_print
from utils.system_util import load_config, sleep


def check_screen(profiles: list[ScoutProfile]) -> Union[ScoutProfile, None]:
    ss = screenshot()
    if ss is None:
        return None
    location = locale_on_screen(profiles, ss)

    if location is None:
        return None
    x, y, p = location
    click_back((x, y))
    return p


def filename_profile(filename):
    # *_c999s_d999.png -> cooltime: 999, detect: 0.999
    # each value optional

    filename = filename.split("/")[-1]
    basename = filename.split(".")[0]
    cooltime = 0
    detect = 0.6
    # use match
    try:
        if "_c" in basename:
            match = re.search(r"_c(\d+)s", basename)
            if match:
                cooltime = int(match.group(1))
        if "_d" in basename:
            detect = float(basename.split("_d")[-1]) / 1000
    except Exception:
        pass

    return cooltime, detect, basename


def to_profile(filename) -> ScoutProfile:
    cooltime, detect, basename = filename_profile(filename)
    return ScoutProfile(basename, cooltime, detect)


def main():
    files, ok, all_files = load_config()
    print("all_files:", all_files)
    print("files:", files)

    if not ok:
        print("Some files are missing. ./scouts/*.png is required.")
        return
    else:
        print(f"All files are loaded. {len(files)} files.")

    mats = get_mats(files)
    profiles = [to_profile(f) for f in files]
    for i, p in enumerate(profiles):
        p.mat = mats[i]

    while True:
        log_print()
        p = check_screen(profiles)
        if p is not None:
            print(f"hit {p.filename}")
            if p.cooltime > 0:
                print(f"cooltime {p.cooltime}")
                sleep(p.cooltime)

        sleep()


if __name__ == "__main__":
    main()
