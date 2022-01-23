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


# sigma = k として，[m - kσ, m + kσ] の範囲にあるデータのインデックスを返す（m : 平均, σ : 標準偏差）
def exclude_outliers(data: List[float], sigma) -> List[int]:
    mean = np.mean(data)
    std = np.std(data)
    res = []
    for i in range(0, len(data)):
        if mean - sigma * std <= data[i] <= mean + sigma * std:
            res.append(i)
    return res


T = TypeVar('T')


def extract_specified_elements(data: List[T], idx: List[int]) -> List[T]:
    res = []
    for i in idx:
        if i < 0 or i >= len(data):
            raise Exception("idx が範囲外")
        res.append(data[i])
    return res
