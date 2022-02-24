from typing import List, TypeVar

import numpy as np


def normalize(data: List[float]) -> List[float]:
    mx = np.nanmax(data)
    mn = np.nanmin(data)
    return list(map(lambda d: (d - mn) / (mx - mn), data))


def standardize(data: List[float]) -> List[float]:
    mean = np.nanmean(data)
    std = np.nanstd(data)
    return list(map(lambda d: (d - mean) / std, data))


# sigma = k として，[m - kσ, m + kσ] の範囲にあるかどうかの Bool 配列を返す（m : 平均, σ : 標準偏差）
# NaN も除外される
def exclude_outliers(data: List[float], sigma: float) -> List[bool]:
    mean = np.nanmean(data)
    std = np.nanstd(data)
    return [
        not np.isnan(d) and mean - sigma * std <= d <= mean + sigma * std for d in data
    ]


# NaN を除外する
def exclude_nan(data: List[float]) -> List[bool]:
    return [not np.isnan(d) for d in data]


T = TypeVar("T")


def extract_specified_elements(data: List[T], mask: List[bool]) -> List[T]:
    return list(map(lambda t: t[0], filter(lambda t: t[1], zip(data, mask))))


def exclude_nan_list(data: List[List[float]]) -> List[bool]:
    return [not np.NaN in d for d in data]
