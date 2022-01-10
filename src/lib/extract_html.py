import requests
from bs4 import BeautifulSoup


def source_code_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    dom = soup.find_all(id="submission-code")
    assert len(dom) == 1
    return dom[0].text


def create_submission_url(contest_id: str, submission_id: int) -> str:
    return "https://atcoder.jp/contests/{}/submissions/{}".format(contest_id, submission_id)


def get_source_code(contest_id: str, submission_id: int) -> str:
    url = create_submission_url(contest_id, submission_id)
    r = requests.get(url)
    if r.ok:
        s = r.text
        s = source_code_extractor(s)
        return s
    else:
        raise Exception(
            "bad request: {} (contest_id: {}, submission_id: {})".format(r.reason, contest_id, submission_id))
