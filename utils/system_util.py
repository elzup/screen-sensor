import sys
import time
import os
from pathlib import Path
from config import path_scouts_files, cooltime_seconds


def path_fix(f):
    return str(Path(f))


def exit():
    sys.exit()


def sleep(s=cooltime_seconds):
    time.sleep(s)


def load_config():
    scouts_files = list(Path(".").glob(path_scouts_files))
    files = list(map(path_fix, scouts_files))
    files = list(filter(os.path.exists, files))

    return files, len(files) > 0.0, scouts_files
