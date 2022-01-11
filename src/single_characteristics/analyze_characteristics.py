from typing import Callable

import numpy as np
import pandas as pd

from src.lib.data_handling import standardize, normalize
from src.lib.submissions import filtered_submissions, load_all_submissions, with_source_codes
from src.single_characteristics.word_count import *
from matplotlib import pyplot as plt


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
def testing(func: Callable[[List[Tuple[Submission, str]]], List[float]], dataset: List[Tuple[Submission, str]],
            file_name: str):
    data_handle = "standardize"
    if data_handle == "normalize":
        features = normalize(func(dataset))
    elif data_handle == "standardize":
        features = standardize(func(dataset))
    else:
        data_handle = "nothing"
        features = func(dataset)
    ratings = []
    for s in dataset:
        ratings.append(s[0].rating)
    # 統計処理をする(相関とか)
    plt.scatter(features, ratings, label="R: {}".format(pd.Series(features).corr(pd.Series(ratings))))
    plt.legend(loc="best")
    plt.xlabel("features")
    plt.ylabel("ratings")
    plt.savefig("figs/{}_{}.pdf".format(data_handle, file_name))
    plt.cla()
    plt.clf()


dataset = sampling()
testing(code_length, dataset, "code_length")
testing(word_count_any("define"), dataset, "wc_define")
testing(word_count_any("using"), dataset, "wc_using")
testing(word_count_any("define int long long"), dataset, "wc_define_int_long_long")
testing(word_count_any("for"), dataset, "wc_for")
# testing(word_count_any_in_main("for"), dataset)
testing(word_count_any("if"), dataset, "wc_if")
# testing(word_count_any_in_main("if"), dataset)
testing(word_count_any("vector"), dataset, "wc_vector")
# testing(word_count_any_in_main("vector"), dataset)
testing(word_count_any("rep"), dataset, "wc_rep")
# testing(word_count_any_in_main("rep"), dataset)
testing(word_count_any("auto"), dataset, "wc_auto")
# testing(word_count_any_in_main("auto"), dataset)
