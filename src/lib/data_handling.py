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


# NaN を除外し，
# sigma = k として，[m - kσ, m + kσ] の範囲にあるかどうかの Bool 配列を返す（m : 平均, σ : 標準偏差）
def exclude_outliers(data: List[float], sigma: float) -> List[bool]:
    mean = np.nanmean(data)
    std = np.nanstd(data)
    return [not np.isnan(data[i]) and mean - sigma * std <= data[i] <= mean + sigma * std for i in
            range(0, len(data))]


T = TypeVar('T')


def extract_specified_elements(data: List[T], mask: List[bool]) -> List[T]:
    return list(map(lambda t: t[0], filter(lambda t: t[1], zip(data, mask))))
