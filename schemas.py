from dataclasses import dataclass
from typing import Optional, Union
import numpy as np

MatLike = Union[np.ndarray]


@dataclass
class ScoutProfile:
    filename: str
    cooltime: int = 0
    detect: float = 0.6  # -1.0 ~ 1.0
    mat: Optional[MatLike] = None
