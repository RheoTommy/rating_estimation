import os.path
import pickle
import time
from typing import List, Tuple

from tqdm import tqdm

from src.lib.extract_html import get_source_code


class Submission:
    def __init__(self, submission_id: int, epoch_second: int, problem_id: str, contest_id: str, user_id: str,
                 is_ac: bool, during_contest: bool, difficulty: int, rating: int):
        self.submission_id = submission_id
        self.epoch_second = epoch_second
        self.problem_id = problem_id
        self.contest_id = contest_id
        self.user_id = user_id
        self.is_ac = is_ac
        self.during_contest = during_contest
        self.difficulty = difficulty
        self.rating = rating

    def __str__(self) -> str:
        return """\
submission_id = {},
epoch_second = {},
problem_id = {},
contest_id = {},
user_id = {},
is_ac = {},
during_contest = {},
difficulty = {},
rating = {}""".format(
            self.submission_id,
            self.epoch_second,
            self.problem_id,
            self.contest_id,
            self.user_id,
            self.is_ac,
            self.during_contest,
            self.difficulty,
            self.rating
        )


def load_all_submissions() -> List[Submission]:
    path = "pickle/submissions.pickle"
    with open(path, "rb") as f:
        pk = pickle.load(f)
        return pk


def save_all_submissions(submissions: List[Submission]):
    with open("pickle/submissions.pickle", "wb") as f:
        pickle.dump(submissions, f)


# [submission] -> [(submission, source_code)]
def get_source_codes(submissions: List[Submission]) -> List[str]:
    def f(submission: Submission) -> str:
        if os.path.isfile("source_codes/{}.cpp".format(submission.submission_id)):
            with open("source_codes/{}.cpp".format(submission.submission_id), "rb") as fi:
                code = fi.read().decode()
                return code

        time.sleep(0.25)
        try:
            source_code = get_source_code(submission.contest_id, submission.submission_id)
        except Exception as e:
            print(e)
            return ""
        else:
            return source_code

    return list(map(f, tqdm(submissions)))


def filtered_submissions(submissions: List[Submission]) -> List[Submission]:
    return list(
        filter(
            lambda submission: submission.during_contest and submission.is_ac and 400 <= submission.difficulty,
            submissions))


def extract_available_submissions(submissions: List[Submission]) -> List[Submission]:
    def f(submission: Submission) -> bool:
        return os.path.isfile("source_codes/{}.cpp".format(submission.submission_id))

    return list(filter(f, tqdm(submissions)))


def load_all_available_submissions() -> List[Submission]:
    with open("pickle/available_submissions.pickle", "rb") as f:
        return pickle.load(f)


def save_all_available_submissions(submissions: List[Submission]):
    with open("pickle/available_submissions.pickle", "wb") as f:
        pickle.dump(submissions, f)
