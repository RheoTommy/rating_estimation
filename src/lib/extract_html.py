from bs4 import BeautifulSoup


def source_code_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    dom = soup.find_all(id="submission-code")
    assert len(dom) == 1
    return dom[0].text


def create_submission_url(contest_id: str, submission_id: str) -> str:
    return "https://atcoder.jp/contests/{}/submissions/{}".format(contest_id, submission_id)
