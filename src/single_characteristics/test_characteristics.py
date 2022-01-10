from src.lib.submissions import Submission, load_all_submissions
from typing import List, Callable
from operator import itemgetter
import numpy as np


def sampling() -> List[Submission]:
    sample_size = 10000
    all_sub = load_all_submissions()
    idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    return itemgetter(*idx)(all_sub)


# func : take dataset, return estimated ratings
def testing(func: Callable[[List[Submission]], List[int]], dataset: List[Submission]):
    estimation = func(dataset)
    # estimation に対する統計処理をする(誤差とか)


# dataset = sampling()
# testing(, dataset)
