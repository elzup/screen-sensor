import re
from typing import Optional, Union

from schemas import ScoutProfile, reset_profiles
from services.gui_service import click_back, screenshot
from services.image_service import get_mats, locale_on_screen_mut
from services.log_service import log_time_print
from utils.system_util import gray, load_config, sleep, basename


def check_screen_mut(scouts: list[ScoutProfile]):
    ss = screenshot()
    if ss is None:
        return
    hit = locale_on_screen_mut(scouts, ss)

    if hit is not None and hit.check is not None:
        click_back((hit.check.px, hit.check.py))


def split_filename(filename):
    filename = basename(filename.split("/")[-1])
    id = filename.split(".")[0]
    return filename, id


def filename_profile(filename):
    # *_c999s_d999.png -> cooltime: 999, detect: 0.999
    # each value optional
    filename, basename = split_filename(filename)

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
    scouts = [to_profile(f) for f in files]
    for i, p in enumerate(scouts):
        p.mat = mats[i]
    while True:
        check_screen_profile(scouts)
        sleep()


def check_screen_profile(scouts: list[ScoutProfile]):
    reset_profiles(scouts)
    hit = check_screen_mut(scouts)
    hit_log(hit, scouts)


def hit_log(hit: Optional[ScoutProfile], scouts: list[ScoutProfile]):
    log_time_print()
    print(" ".join(map(ScoutProfile.head, scouts)))
    print(" ".join(map(ScoutProfile.score, scouts)))
    if hit is None:
        return
    print(f"hit {hit.filename}")
    if hit.cooltime > 0:
        print(f"cooltime {hit.cooltime}")
        sleep(hit.cooltime)


if __name__ == "__main__":
    main()
