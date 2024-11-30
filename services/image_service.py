from functools import partial
from typing import Iterable, Optional, TypeVar, Union

import cv2
import numpy as np

from schemas import CheckResult, MatLike, ScoutProfile


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


T = TypeVar("T")


def find(a: Iterable[T]) -> Optional[T]:
    return next(filter(bool, a), None)


def locale_on_screen_mut(scouts: list[ScoutProfile], screenshot):
    screenshot = grayscale_patch_ss(screenshot)
    screen_match = partial(template_match, screenshot=screenshot)

    find_mat = None

    for scout in scouts:
        res = screen_match(scout)
        if res is not None:
            find_mat = res
            break

    return find_mat
    # return find(map(scrren_match, scouts))


def template_match(scout: ScoutProfile, screenshot) -> Optional[CheckResult]:
    if scout.mat is None:
        return None
    # テンプレートマッチング
    result = cv2.matchTemplate(screenshot, scout.mat, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    # print(f"{max_val=}, {max_loc}")
    return CheckResult(
        max_val >= scout.detect,
        max_val,
        max_loc[0] + scout.mat.shape[1] // 2,
        max_loc[1] + scout.mat.shape[0] // 2,
    )
