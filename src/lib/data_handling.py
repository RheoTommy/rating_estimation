from typing import List

import numpy as np


def normalize(data: List[float]):
    mx = np.max(data)
    mn = np.min(data)
    return list(map(lambda d: (d - mn) / (mx - mn), data))


def standardize(data: List[float]):
    mean = np.mean(data)
    std = np.std(data)
    return list(map(lambda d: (d - mean) / std, data))
