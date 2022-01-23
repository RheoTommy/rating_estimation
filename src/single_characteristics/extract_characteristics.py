from typing import List, Tuple, Callable
from src.lib.submissions import Submission
from src.lib.source_code_handling import extract_str_in_main, exclude_comments


def word_count_any(word: str) -> Callable[[List[Tuple[Submission, str]]], List[float]]:
    def f(dataset: List[Tuple[Submission, str]]) -> List[float]:
        res = []
        for _, code in dataset:
            code = exclude_comments(code)
            res.append(code.count(word))
        return res

    return f


def word_count_any_in_main(word: str, do_print_errors: bool = False) -> Callable[
    [List[Tuple[Submission, str]]], List[float]]:
    def f(dataset: List[Tuple[Submission, str]]) -> List[float]:
        res = []
        error = 0
        for submission, code in dataset:
            code = exclude_comments(code)
            try:
                res.append((extract_str_in_main(code)).count(word))
            except Exception as e:
                error += 1
                res.append(0.0)
                if do_print_errors:
                    print(e)
                    print("submission id: {}".format(submission.submission_id))
        print("Error {}/{}".format(error, len(dataset)))
        return res

    return f


def code_length(dataset: List[Tuple[Submission, str]]) -> List[float]:
    return list(map(lambda x: len(x[1]), dataset))
