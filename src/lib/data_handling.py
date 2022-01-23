from typing import List, TypeVar

import numpy as np


def normalize(data: List[float]) -> List[float]:
    mx = np.max(data)
    mn = np.min(data)
    return list(map(lambda d: (d - mn) / (mx - mn), data))


def standardize(data: List[float]) -> List[float]:
    mean = np.mean(data)
    std = np.std(data)
    return list(map(lambda d: (d - mean) / std, data))


# sigma = k として，[m - kσ, m + kσ] の範囲にあるかどうかの Bool 配列を返す（m : 平均, σ : 標準偏差）
def exclude_outliers(data: List[float], sigma: float) -> List[bool]:
    mean = np.mean(data)
    std = np.std(data)
    return [mean - sigma * std <= data[i] <= mean + sigma * std for i in range(0, len(data))]


T = TypeVar('T')


def extract_specified_elements(data: List[T], mask: List[bool]) -> List[T]:
    return list(map(lambda t: t[0], filter(lambda t: t[1], zip(data, mask))))
