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


def locale_on_screen_mut(
    scouts: list[ScoutProfile], screenshot, size
) -> Optional[ScoutProfile]:
    screenshot = grayscale_patch_ss(screenshot)
    screen_match = partial(template_match, screenshot=screenshot, size=size)

    find_mat = None

    for scout in scouts:
        res = screen_match(scout)
        scout.check = res
        if res is not None and res.hit:
            find_mat = scout
            break

    return find_mat
    # return find(map(scrren_match, scouts))


def template_match(
    scout: ScoutProfile, screenshot, size
) -> Optional[CheckResult]:
    if scout.mat is None:
        return None
    result = cv2.matchTemplate(screenshot, scout.mat, cv2.TM_CCOEFF_NORMED)
    # max_val
    _, value, _, [x, y] = cv2.minMaxLoc(result)
    return CheckResult(
        value >= scout.detect,
        value,
        x + scout.mat.shape[1] // 2,
        y + scout.mat.shape[0] // 2,
        h=size[0],
        w=size[1],
    )
