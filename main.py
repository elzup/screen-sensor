import re
from typing import Optional

from schemas import ScoutProfile, reset_profiles
from services.gui_service import (
    click_back,
    screen_size,
    screenshot,
    GuiException,
)
from services.image_service import get_mats, locale_on_screen_mut
from services.log_service import log_time_print
from utils.plot import draw_grid_with_mark
from utils.system_util import gray, load_config, sleep, basename


def check_screen_mut(scouts: list[ScoutProfile]):
    ss = screenshot()
    size = screen_size()

    if ss is None:
        return
    hit = locale_on_screen_mut(scouts, ss, size)
    # width, height = ss.size

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


def filter_none(l):
    return [x for x in l if x is not None]


def hit_log(hit: Optional[ScoutProfile], scouts: list[ScoutProfile]):
    log_time_print()
    if len(scouts) == 0:
        return
    print(" ".join(map(ScoutProfile.head, scouts)))
    print(" ".join(map(ScoutProfile.score, scouts)))
    s = scouts[0].check
    if s is not None:
        print(
            draw_grid_with_mark(
                s.h, s.w, filter_none([s.check for s in scouts])
            )
        )

    if hit is None:
        return
    print(f"hit {hit.filename}")
    if hit.cooltime > 0:
        print(f"cooltime {hit.cooltime}")
        sleep(hit.cooltime)


def keep_main():
    while True:
        try:
            main()
        except GuiException as e:
            print(f"GuiException: {e}")


if __name__ == "__main__":
    try:
        keep_main()
    except KeyboardInterrupt:
        print("Bye")
        exit(0)
