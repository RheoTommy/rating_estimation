import os.path
import time
from typing import List

import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

from src.lib.submissions import (
    load_all_submissions,
    Submission,
)


def source_code_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    dom = soup.find_all(id="submission-code")
    assert len(dom) == 1
    return dom[0].text


def create_submission_url(contest_id: str, submission_id: int) -> str:
    return "https://atcoder.jp/contests/{}/submissions/{}".format(
        contest_id, submission_id
    )


def get_source_code(contest_id: str, submission_id: int) -> str:
    url = create_submission_url(contest_id, submission_id)
    r = requests.get(url)
    if r.ok:
        s = r.text
        s = source_code_extractor(s)
        return s
    else:
        raise Exception(
            "bad request: {} (contest_id: {}, submission_id: {})".format(
                r.reason, contest_id, submission_id
            )
        )


def filtered_submissions(submissions: List[Submission]) -> List[Submission]:
    return list(
        filter(
            lambda submission: submission.during_contest
                               and submission.is_ac
                               and 400 <= submission.difficulty,
            submissions,
        )
    )


def get_all_source_codes():
    submissions = load_all_submissions()
    submissions = filtered_submissions(submissions)
    for submission in tqdm(submissions):
        if os.path.isfile("source_codes/{}.cpp".format(submission.submission_id)):
            continue
        for _ in range(5):
            try:
                time.sleep(0.25)
                source_code = get_source_code(
                    submission.contest_id, submission.submission_id
                )
                with open(
                        "source_codes/{}.cpp".format(submission.submission_id), "wb"
                ) as f:
                    f.write(source_code.encode())
            except Exception as e:
                tqdm.write(e)
            else:
                break
