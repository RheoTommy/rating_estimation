from typing import List, Tuple
from src.lib.submissions import Submission
from src.lib.source_code_handling import extract_str_in_main


def code_length(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return list(map(lambda x: len(x[1]), dataset))


def word_count(dataset: List[Tuple[Submission, str]], word: str) -> List[float]:
    res = []
    for _, code in dataset:
        res.append(code.count(word))
    return res


def word_count_in_main(dataset: List[Tuple[Submission, str]], word: str) -> List[float]:
    res = []
    for _, code in dataset:
        try:
            res.append(extract_str_in_main(code).count(word))
        except Exception as e:
            print(e)
            res.append(0)

    return res


def word_count_define(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "define")


def word_count_using(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "using")


def word_count_define_int_long_long(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "define int long long")


def word_count_for(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "for")


def word_count_in_main_for(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count_in_main(dataset, "for")


def word_count_if(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "if")


def word_count_in_main_if(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count_in_main(dataset, "if")


def word_count_vector(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "vector")


def word_count_in_main_vector(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count_in_main(dataset, "vector")


def word_count_rep(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "rep")


def word_count_in_main_rep(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count_in_main(dataset, "rep")


def word_count_auto(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count(dataset, "auto")


def word_count_in_main_auto(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return word_count_in_main(dataset, "auto")
