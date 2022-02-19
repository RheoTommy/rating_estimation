import os.path
import pickle
from typing import List, Tuple

from tqdm import tqdm


class Submission:
    def __init__(
            self,
            submission_id: int,
            epoch_second: int,
            problem_id: str,
            contest_id: str,
            user_id: str,
            is_ac: bool,
            during_contest: bool,
            difficulty: int,
            rating: int,
    ):
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
            self.rating,
        )


def load_all_submissions() -> List[Submission]:
    path = "pickle/submissions.pickle"
    with open(path, "rb") as f:
        pk = pickle.load(f)
        return pk


def save_all_submissions(submissions: List[Submission]):
    with open("pickle/submissions.pickle", "wb") as f:
        pickle.dump(submissions, f)


# [submission] -> [(source code, preprocessed code, assembler)]
def get_source_codes(submissions: List[Submission]) -> List[Tuple[str, str, str]]:
    def f(submission: Submission) -> Tuple[str, str, str]:
        if os.path.isfile("source_codes/{}.cpp".format(submission.submission_id)):
            with open(
                    "source_codes/{}.cpp".format(submission.submission_id), "rb"
            ) as fi:
                code = fi.read().decode()
        else:
            raise Exception("ソースコードがローカルにありません！")
        if os.path.isfile("pp/{}.cpp".format(submission.submission_id)):
            with open(
                    "pp/{}.cpp".format(submission.submission_id), "rb"
            ) as fi:
                pp = fi.read().decode()
        else:
            raise Exception("プリプロセス後コードがローカルにありません！")
        if os.path.isfile("assembler/{}.s".format(submission.submission_id)):
            with open(
                    "assembler/{}.s".format(submission.submission_id), "rb"
            ) as fi:
                asm = fi.read().decode()
        else:
            raise Exception("アセンブラがローカルにありません！")
        return code, pp, asm

    return list(map(f, tqdm(submissions)))


def load_all_available_submissions() -> List[Submission]:
    with open("pickle/available_submissions.pickle", "rb") as f:
        return pickle.load(f)


def save_all_available_submissions(submissions: List[Submission]):
    with open("pickle/available_submissions.pickle", "wb") as f:
        pickle.dump(submissions, f)


def filter_with_problem_id(
        submissions: List[Submission], problem_id: str
) -> List[Submission]:
    return list(
        filter(lambda submission: submission.problem_id == problem_id, submissions)
    )
