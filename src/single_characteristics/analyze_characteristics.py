from typing import Tuple

import pandas as pd
import seaborn as sns
from tqdm import tqdm

from src.lib.data_handling import (
    standardize,
    normalize,
    exclude_outliers,
    extract_specified_elements,
)
from src.lib.submissions import get_source_codes, load_all_available_submissions
from src.single_characteristics.extract_characteristics import *
from matplotlib import pyplot as plt

fan = [
    (word_count_any_parallel("define"), "wc_define"),
    (word_count_any_parallel("using"), "wc_using"),
    (word_count_any_parallel("define int long long"), "wc_define_int_long_long"),
    (word_count_any_parallel("for"), "wc_for"),
    (word_count_any_parallel("if"), "wc_if"),
    (word_count_any_parallel("vector"), "wc_vector"),
    (word_count_any_parallel("rep"), "wc_rep"),
    (word_count_any_parallel("auto"), "wc_auto"),
    (word_count_any_in_main_parallel("for"), "wc(main)_for"),
    (word_count_any_in_main_parallel("if"), "wc(main)_if"),
    (word_count_any_in_main_parallel("vector"), "wc(main)_vector"),
    (word_count_any_in_main_parallel("rep"), "wc(main)_rep"),
    (word_count_any_in_main_parallel("auto"), "wc(main)_auto"),
    (code_length, "code_length"),
    (code_length_in_main, "code_length_in_main"),
    (comments_ratio, "comments_ratio"),
]

data_handle_funcs_and_names = [
    (standardize, "standardize"),
    (normalize, "normalize"),
    (lambda x: x, "nothing"),
]


def sampling() -> Tuple[List[Submission], List[str]]:
    sample_size = 5000
    # 提出データのローカル保存が終わったら
    all_sub = load_all_available_submissions()
    idx = np.random.choice(np.arange(len(all_sub)), sample_size, replace=False)
    sample_sub = []
    for i in idx:
        sample_sub.append(all_sub[i])
    print("start getting source codes")
    source_codes = get_source_codes(sample_sub)
    print("finish getting source codes")
    return sample_sub, source_codes


# func: [(Submission, str)]) -> (features: [float])
# data_handle_func: [float] -> [float]
def test_one_characteristic(
        submissions: List[Submission],
        source_codes: List[str],
        func: Callable[[List[str]], List[float]],
        file_name: str,
        data_handle_func: Callable[[List[float]], List[float]] = standardize,
        data_handle_name: str = "standardize",
        do_exclude_outliers: bool = True,
        sigma: float = 2,
):
    features = data_handle_func(func(source_codes))
    ratings = list(map(lambda submission: submission.rating, submissions))
    if do_exclude_outliers:
        mask = exclude_outliers(features, sigma)
        features = extract_specified_elements(features, mask)
        ratings = extract_specified_elements(ratings, mask)
    # 統計処理をする(相関とか)
    plt.scatter(
        features,
        ratings,
        label="R: {}".format(pd.Series(features).corr(pd.Series(ratings))),
    )
    plt.legend(loc="best")
    plt.xlabel("features")
    plt.ylabel("ratings")
    plt.savefig("figs/{}_{}.png".format(data_handle_name, file_name))
    plt.cla()
    plt.clf()

    print(
        "finished testing characteristic {} (data_handle: {})".format(
            file_name, data_handle_name
        )
    )


def save_pair_plot(
        submissions: List[Submission],
        source_codes: List[str],
        funcs_and_names: List[Tuple[Callable[[List[str]], List[float]], str]],
        png_file_name: str = "pair_plot",
):
    print("started testing all characteristics")

    df = pd.DataFrame(
        {"ratings": list(map(lambda submission: submission.rating, submissions))}
    )
    mask = [True for _ in range(len(submissions))]
    for (func, func_name) in tqdm(funcs_and_names):
        features = func(source_codes)
        mask = list(
            map(lambda t: t[0] and t[1], zip(mask, exclude_outliers(features, 2)))
        )
        df[func_name] = features
    df = df[mask]

    print(df.corr())

    sns.pairplot(df)
    plt.savefig("figs/{}.png".format(png_file_name))
    plt.clf()
    plt.cla()

    print("finished testing all characteristics and saved pair plot figure")


def test_characteristics():
    submissions, source_codes = sampling()

    save_pair_plot(submissions, source_codes, fan)

    for (f, fn) in fan:
        for (hf, hfn) in data_handle_funcs_and_names:
            test_one_characteristic(submissions, source_codes, f, fn, hf, hfn)

    print("all processes finished")
