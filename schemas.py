from dataclasses import dataclass
from typing import Optional, Union
import numpy as np

from utils.system_util import gray

MatLike = Union[np.ndarray]


@dataclass
class CheckResult:
    hit: bool
    value: float
    px: int
    py: int


@dataclass
class ScoutProfile:
    filename: str
    cooltime: int = 0
    detect: float = 0.6  # -1.0 ~ 1.0
    mat: Optional[MatLike] = None
    check: Optional[CheckResult] = None

    def head(self):
        return gray(f"{self.filename[:5]}")


def reset_profiles(profiles):
    for p in profiles:
        p.check = None
    return profiles
