from src.lib.submissions import Submission, filtered_submissions, load_all_submissions, with_source_codes
from src.lib.data_handling import standardize
from typing import Callable, List, Tuple
import numpy as np


def sampling() -> List[Tuple[Submission, str]]:
    sample_size = 1
    all_sub = filtered_submissions(load_all_submissions())
    idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    sample_sub = []
    for i in idx:
        sample_sub.append(all_sub[i])
    print("start getting source codes")
    res = with_source_codes(sample_sub)
    print("finish getting source codes")
    # 提出データのローカル保存が終われば，このまま return res すれば良い
    res2 = []
    for sub, s in res:
        if s != "":
            res2.append((sub, s))
    print("available data count : {}".format(len(res2)))
    return res2


# func : (dataset: List[Submission]) -> (features: List[float])
def testing(func: Callable[[List[Submission]], List[float]], dataset: List[Submission]):
    features = standardize(func(dataset))
    ratings = []
    for s in dataset:
        ratings.append(s.rating)
    # 統計処理をする(相関とか)


dataset = sampling()
# testing(, dataset)
