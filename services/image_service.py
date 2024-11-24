from functools import partial
from typing import Iterable, Union
import cv2
import numpy as np

MatLike = Union[np.ndarray]


def get_mat(path):
    return cv2.imread(path, cv2.IMREAD_UNCHANGED)


def grayscale_patch(mat: MatLike):
    if mat.shape[2] == 4:  # RGBAの場合
        mat = cv2.cvtColor(mat, cv2.COLOR_BGRA2GRAY)
    elif len(mat.shape) == 3:  # RGBの場合
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    return mat


def grayscale_patch_ss(ss: MatLike):
    ss = np.array(ss)  # PILからnumpy配列に変換
    return grayscale_patch(ss)


def get_mats(paths):
    mats = [get_mat(p) for p in paths]
    # テンプレートがRGBAの場合、グレースケールに変換
    return list(map(grayscale_patch, mats))


def find(a: Iterable):
    return next(filter(bool, a), None)


def locale_on_screen(mats, screenshot):
    screenshot = grayscale_patch_ss(screenshot)
    scrren_match = partial(template_match, screenshot=screenshot)

    return find(map(scrren_match, mats))


def template_match(mat: MatLike, screenshot) -> Union[None, tuple[int, int]]:

    # テンプレートマッチング
    result = cv2.matchTemplate(screenshot, mat, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(f"{min_val=}, {max_val=}, {min_loc=}, {max_loc=}")
    if max_val >= 0.6:
        return (
            max_loc[0] + mat.shape[1] // 2,
            max_loc[1] + mat.shape[0] // 2,
        )
    return None
