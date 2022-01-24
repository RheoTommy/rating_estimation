from typing import List, Callable

import numpy as np

from src.lib.submissions import Submission
from src.lib.source_code_handling import extract_str_in_main, exclude_comments
from joblib import Parallel, delayed


def word_count_any(word: str) -> Callable[[List[str]], List[float]]:
    def f(source_codes: List[str]) -> List[float]:
        res = []
        for code in source_codes:
            code = exclude_comments(code)
            res.append(code.count(word))
        return res

    return f


def word_count_any_in_main(word: str, do_print_errors: bool = False) -> Callable[
    [List[str]], List[float]]:
    def f(source_codes: List[str], submissions: List[Submission] = None) -> List[float]:
        res = []
        error = 0
        for i in range(len(source_codes)):
            code = source_codes[i]
            code = exclude_comments(code)
            try:
                res.append((extract_str_in_main(code)).count(word))
            except Exception as e:
                error += 1
                res.append(np.nan)
                if do_print_errors:
                    print(e)
                    if not (submissions is None):
                        print("submission id: {}".format(submissions[i].submission_id))
        print("Error {}/{}".format(error, len(source_codes)))
        return res

    return f


def word_count_any_parallel(word: str) -> Callable[[List[str]], List[float]]:
    def f(source_codes: List[str]) -> List[float]:
        def sub_f(code: str) -> float:
            code = exclude_comments(code)
            return code.count(word)

        return Parallel(n_jobs=-1)(delayed(sub_f)(t) for t in source_codes)

    return f


# 多分 source_codes には [str] じゃなくて tqdm[str] が送られるので添え字アクセスすると死ぬ
def word_count_any_in_main_parallel(word: str, do_print_errors: bool = False) -> Callable[[List[str]], List[float]]:
    def f(source_codes: List[str]) -> List[float]:
        def sub_f(code: str) -> float:
            code = exclude_comments(code)
            try:
                return extract_str_in_main(code).count(word)
            except Exception as e:
                if do_print_errors:
                    print(e)
                return np.nan

        return Parallel(n_jobs=-1)(delayed(sub_f)(source_code) for source_code in source_codes)

    return f


def code_length(source_codes: List[str]) -> List[float]:
    return list(map(len, source_codes))


def comments_ratio(source_codes: List[str]) -> List[float]:
    def f(code: str) -> float:
        ori = len(code)
        com = ori - len(exclude_comments(code))
        return com / ori

    return list(map(f, source_codes))
