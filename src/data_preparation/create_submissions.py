from typing import List

import numpy as np
import pandas as pd
from tqdm import tqdm
from pandas import DataFrame

from src.lib.problems import get_difficulty, is_during_contest
from src.lib.submissions import Submission, save_all_submissions
from src.lib.user import get_rating


def convert_csv_to_submissions(df: DataFrame) -> List[Submission]:
    print('extracting "id" column')
    submission_id_list = df["id"].to_numpy(dtype="int64").tolist()
    print('extracting "epoch_second" column')
    epoch_second_list = df["epoch_second"].to_numpy(dtype="int64").tolist()
    print('extracting "problem_id" column')
    problem_id_list = df["problem_id"].to_numpy(dtype="str").tolist()
    print('extracting "contest_id" column')
    contest_id_list = df["contest_id"].to_numpy(dtype="str").tolist()
    print('extracting "user_id" column')
    user_id_list = df["user_id"].to_numpy(dtype="str").tolist()
    print('extracting "result" column')
    is_ac_list = np.vectorize(lambda res: res == "AC")(
        df["result"].to_numpy(dtype="str")
    ).tolist()

    is_during_contest_queries = list(zip(contest_id_list, epoch_second_list))
    get_difficulty_queries = problem_id_list
    get_rating_queries = list(zip(user_id_list, epoch_second_list))

    print('getting "during contest"')
    during_contest_list = is_during_contest(is_during_contest_queries)
    print('getting "difficulty"')
    difficulty_queries_list = get_difficulty(get_difficulty_queries)

    print('getting "rating"')
    rating_list = get_rating(get_rating_queries)

    submissions = []
    print("creating submission list")
    for i in tqdm(range(len(submission_id_list))):
        submissions.append(
            Submission(
                submission_id_list[i],
                epoch_second_list[i],
                problem_id_list[i],
                contest_id_list[i],
                user_id_list[i],
                is_ac_list[i],
                during_contest_list[i],
                difficulty_queries_list[i],
                rating_list[i],
            )
        )
    return submissions


def create_submissions():
    file_name = "csv/extract.csv"
    df = pd.read_csv(file_name)
    submissions = convert_csv_to_submissions(df)
    save_all_submissions(submissions)
    for i in range(min(10, len(submissions))):
        print(submissions[i])


create_submissions()
