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

    def head(self) -> str:
        return gray(f"{self.filename[:7].ljust(5)}")

    def score(self) -> str:
        if self.check is None:
            return gray("----")
        deco = gray if self.check.value < 0.7 else str
        # 0.9876 -> 98.8
        sc = f"{(self.check.value * 100):.1f}".ljust(2)
        den = f"{(self.detect * 100):.0f}".ljust(2)
        return deco(f"{sc}/{den}")


def reset_profiles(profiles):
    for p in profiles:
        p.check = None
    return profiles
