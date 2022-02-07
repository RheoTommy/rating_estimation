from src.lib.data_handling import (
    standardize,
    normalize,
)
from src.single_characteristics.extract_characteristics import (
    word_count_any_parallel,
    word_count_any_in_main_parallel,
    code_length,
    code_length_in_main,
    comments_ratio,
)

characteristics = [
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
