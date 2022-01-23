import numpy as np
import pandas as pd

from src.lib.data_handling import standardize, normalize
from src.lib.submissions import with_source_codes, load_all_available_submissions
from src.single_characteristics.word_count import *
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
def testing(func: Callable[[List[Tuple[Submission, str]]], List[float]], dataset: List[Tuple[Submission, str]],
            file_name: str):
    data_handle = ""
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


d = sampling()
testing(code_length, d, "code_length")
testing(word_count_any("define"), d, "wc_define")
testing(word_count_any("using"), d, "wc_using")
testing(word_count_any("define int long long"), d, "wc_define_int_long_long")
testing(word_count_any("for"), d, "wc_for")
testing(word_count_any_in_main("for"), d, "wc(main)_for")
testing(word_count_any("if"), d, "wc_if")
testing(word_count_any_in_main("if"), d, "wc(main)_if")
testing(word_count_any("vector"), d, "wc_vector")
testing(word_count_any_in_main("vector"), d, "wc(main)_vector")
testing(word_count_any("rep"), d, "wc_rep")
testing(word_count_any_in_main("rep"), d, "wc(main)_rep")
testing(word_count_any("auto"), d, "wc_auto")
testing(word_count_any_in_main("auto"), d, "wc(main)_auto")
