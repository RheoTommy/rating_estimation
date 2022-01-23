from typing import Callable, List, Tuple

import numpy as np
import pandas as pd

from src.lib.data_handling import standardize, normalize, exclude_outliers
from src.lib.submissions import with_source_codes, load_all_available_submissions
from src.single_characteristics.extract_characteristics import *
from matplotlib import pyplot as plt


def sampling() -> List[Tuple[Submission, str]]:
    sample_size = 5000
    # 提出データのローカル保存が終わったら
    all_sub = load_all_available_submissions()
    idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    sample_sub = []
    for i in idx:
        sample_sub.append(all_sub[i])
    print("start getting source codes")
    res = with_source_codes(sample_sub)
    print("finish getting source codes")
    return res


# func : (dataset: List[Tuple[Submission, str]]) -> (features: List[float])
def testing(dataset: List[Tuple[Submission, str]], func: Callable[[List[Tuple[Submission, str]]], List[float]],
            file_name: str, data_handle_func: Callable[[List[float]], List[float]] = standardize,
            data_handle_name: str = "standardize", do_exclude_outliers=True, sigma=1):
    features = data_handle_func(func(dataset))
    features = exclude_outliers(features, sigma)
    ratings = []
    for s in dataset:
        ratings.append(s[0].rating)
    # 統計処理をする(相関とか)
    plt.scatter(features, ratings, label="R: {}".format(pd.Series(features).corr(pd.Series(ratings))))
    plt.legend(loc="best")
    plt.xlabel("features")
    plt.ylabel("ratings")
    plt.savefig("figs/{}_{}.pdf".format(data_handle_name, file_name))
    plt.cla()
    plt.clf()


d = sampling()

testing(d, code_length, "code_length")

funcs_and_names = [
    (word_count_any("define"), "wc_define"),
    (word_count_any("using"), "wc_using"),
    (word_count_any("define int long long"), "wc_define_int_long_long"),
    (word_count_any("for"), "wc_for"),
    (word_count_any("if"), "wc_if"),
    (word_count_any("vector"), "wc_vector"),
    (word_count_any("rep"), "wc_rep"),
    (word_count_any("auto"), "wc_auto"),
    (word_count_any_in_main("for"), "wc(main)_for"),
    (word_count_any_in_main("if"), "wc(main)_if"),
    (word_count_any_in_main("vector"), "wc(main)_vector"),
    (word_count_any_in_main("rep"), "wc(main)_rep"),
    (word_count_any_in_main("auto"), "wc(main)_auto"),
]

data_handle_funcs_and_names = [
    (standardize, "standardize"),
    (normalize, "normalize"),
    (lambda x: x, "nothing"),
]

for (f, fn) in funcs_and_names:
    for (hf, hfn) in data_handle_funcs_and_names:
        testing(d, f, fn, hf, hfn)
