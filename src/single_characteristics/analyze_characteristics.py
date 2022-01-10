from src.lib.submissions import Submission, filtered_submissions, load_all_submissions, load_all_available_submissions, \
    with_source_codes
from src.lib.data_handling import standardize
from typing import Callable, List, Tuple
import numpy as np


def sampling() -> List[Tuple[Submission, str]]:
    sample_size = 1
    # 提出データのローカル保存が終わるまで
    all_sub = filtered_submissions(load_all_submissions())
    idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    sample_sub = []
    for i in idx:
        sample_sub.append(all_sub[i])
    print("start getting source codes")
    res = with_source_codes(sample_sub)
    print("finish getting source codes")
    res = list(filter(lambda x: x[1] != "", res))
    print("available data count : {}".format(len(res)))
    return res
    # 提出データのローカル保存が終わったら
    # all_sub = load_all_available_submissions()
    # idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    # sample_sub = []
    # for i in idx:
    #     sample_sub.append(all_sub[i])
    # print("start getting source codes")
    # res = with_source_codes(sample_sub)
    # print("finish getting source codes")
    # return res


# func : (dataset: List[Submission]) -> (features: List[float])
def testing(func: Callable[[List[Submission]], List[float]], dataset: List[Submission]):
    features = standardize(func(dataset))
    ratings = []
    for s in dataset:
        ratings.append(s.rating)
    # 統計処理をする(相関とか)


dataset = sampling()
# testing(, dataset)
