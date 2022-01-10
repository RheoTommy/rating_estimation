from typing import Callable

import numpy as np

from src.lib.data_handling import standardize
from src.lib.submissions import filtered_submissions, load_all_submissions, with_source_codes
from word_count import *


def sampling() -> List[Tuple[Submission, str]]:
    sample_size = 500
    # 提出データのローカル保存が終わるまで
    all_sub = filtered_submissions(load_all_submissions())
    idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    sample_sub = []
    for i in idx:
        sample_sub.append(all_sub[i])
    print("start getting source codes")
    res = with_source_codes(sample_sub)
    print("finish getting source codes")
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


# func : (dataset: List[Tuple[Submission, str]]) -> (features: List[float])
def testing(func: Callable[[List[Tuple[Submission, str]]], List[float]], dataset: List[Tuple[Submission, str]]):
    features = standardize(func(dataset))
    ratings = []
    for s in dataset:
        ratings.append(s[0].rating)
    # 統計処理をする(相関とか)


dataset = sampling()
testing(code_length, dataset)
testing(word_count_define, dataset)
testing(word_count_using, dataset)
testing(word_count_define_int_long_long, dataset)
testing(word_count_for, dataset)
testing(word_count_in_main_for, dataset)
testing(word_count_if, dataset)
testing(word_count_in_main_if, dataset)
testing(word_count_vector, dataset)
testing(word_count_in_main_vector, dataset)
testing(word_count_rep, dataset)
testing(word_count_in_main_rep, dataset)
testing(word_count_auto, dataset)
testing(word_count_in_main_auto, dataset)
