import os.path
import pickle
from collections import defaultdict
from typing import List, Tuple

import numpy as np
from tqdm import tqdm

from src.lib.data_handling import exclude_nan_list


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


# [submission] -> ([source codes], [assemblers])
def get_source_codes(submissions: List[Submission]) -> Tuple[List[str], List[str]]:
    def f(submission: Submission) -> str:
        if os.path.isfile("source_codes/{}.cpp".format(submission.submission_id)):
            with open(
                    "source_codes/{}.cpp".format(submission.submission_id), "rb"
            ) as fi:
                return fi.read().decode()
        else:
            raise Exception("ソースコードがローカルにありません！")

    def g(submission: Submission) -> str:
        if os.path.isfile("assembler/{}.s".format(submission.submission_id)):
            with open("assembler/{}.s".format(submission.submission_id), "rb") as fi:
                return fi.read().decode()
        else:
            raise Exception("アセンブラがローカルにありません！")

    return list(map(f, tqdm(submissions, desc="getting .cpp", leave=False))), list(
        map(g, tqdm(submissions, desc="getting .s", leave=False)))


def get_characteristics(submissions: List[Submission]) -> List[List[float]]:
    def f(submission: Submission) -> List[float]:
        if os.path.isfile("characteristics/{}.pickle".format(submission.submission_id)):
            with open("characteristics/{}.pickle".format(submission.submission_id), "rb") as fi:
                return pickle.load(fi)
        else:
            raise Exception("特徴量がローカルにありません！")

    return list(map(f, tqdm(submissions, desc="getting characteristics", leave=False)))


def load_not_nan_submissions_and_characteristics() -> Tuple[List[Submission], List[List[float]]]:
    submissions = load_all_available_submissions()
    chara = get_characteristics(submissions)
    mask = np.array(exclude_nan_list(chara))
    submissions = np.array(submissions)[mask]
    chara = np.array(chara)[mask]
    return submissions, chara


def load_train_data(make_y_list: bool = False) -> Tuple[List[List[float]], List[List[float]]]:
    submissions, chara = load_not_nan_submissions_and_characteristics()
    return chara, [[submission.rating] if make_y_list else submission.rating for submission in submissions]


def load_train_data_based_person() -> Tuple[List[List[float]], List[List[List[float]]]]:
    submissions, characteristics = load_not_nan_submissions_and_characteristics()
    chara = defaultdict(lambda: [])
    for sub, ch in tqdm(zip(submissions, characteristics), desc="grouping by user_id"):
        chara[sub.user_id].append((sub.rating, ch))
    v = list(chara.values())
    x = []
    y = []
    for vi in v:
        xv = []
        yv = []
        for yi, xi in vi:
            xv.append(xi)
            yv.append(yi)
        x.append(xv)
        y.append(yv)
    return y, x


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
