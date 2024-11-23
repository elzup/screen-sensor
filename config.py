import sys
import time
import os
from pathlib import Path


def path_fix(f):
    return str(Path(f))


def exit():
    sys.exit()


def cooltime():
    time.sleep(10)


def load_config():
    scouts_files = list(Path("./scouts").rglob("*.png"))
    files = list(map(path_fix, scouts_files))
    files = list(filter(os.path.exists, files))

    return files, len(files) > 0.0


def log_print():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
