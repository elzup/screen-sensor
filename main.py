from utils.system_util import cooltime, load_config
from services.log_service import log_print
from services.gui_service import click_back, screenshot
from services.image_service import get_mats, locale_on_screen


def check_screen(mats):
    ss = screenshot()
    if ss is None:
        return
    location = locale_on_screen(mats, ss)

    if location is not None:
        click_back(location)


def main():
    files, ok, filenames = load_config()
    print(filenames)

    if not ok:
        print("Some files are missing. ./scouts/*.png is required.")
        return
    else:
        print(f"All files are loaded. {len(files)} files.")

    mats = get_mats(files)

    while True:
        check_screen(mats)

        log_print()
        cooltime()


if __name__ == "__main__":
    main()
