from typing import List, Tuple, Callable
from src.lib.submissions import Submission
from src.lib.source_code_handling import extract_str_in_main


def word_count_any(word: str) -> Callable[[List[Tuple[Submission, str]]], List[float]]:
    def f(dataset: List[Tuple[Submission, str]]) -> List[float]:
        res = []
        for _, code in dataset:
            res.append(code.count(word))
        return res

    return f


def word_count_any_in_main(word: str) -> Callable[[List[Tuple[Submission, str]]], List[float]]:
    def f(dataset: List[Tuple[Submission, str]]) -> List[float]:
        res = []
        for _, code in dataset:
            res.append((extract_str_in_main(code)).count(word))
        return res

    return f


def code_length(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return list(map(lambda x: len(x[1]), dataset))
