from config import cooltime, load_config, log_print
from gui_util import click, screenshot
from image_util import get_mats, locale_on_screen


def check_screen(mats):
    ss = screenshot()
    location = locale_on_screen(mats, ss)

    if location is not None:
        click(location)


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
