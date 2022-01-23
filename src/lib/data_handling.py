from typing import List

import numpy as np


def normalize(data: List[float]) -> List[float]:
    mx = np.max(data)
    mn = np.min(data)
    return list(map(lambda d: (d - mn) / (mx - mn), data))


def standardize(data: List[float]) -> List[float]:
    mean = np.mean(data)
    std = np.std(data)
    return list(map(lambda d: (d - mean) / std, data))


# sigma = k として，[m - kσ, m + kσ] の範囲のデータだけ取る（m : 平均, σ : 標準偏差）
def exclude_outliers(data: List[float], sigma=1) -> List[float]:
    mean = np.mean(data)
    std = np.std(data)
    return list(filter(lambda x: mean - sigma * std <= x <= mean + sigma * std, data))
