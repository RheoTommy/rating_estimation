from bs4 import BeautifulSoup
import requests


def source_code_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    dom = soup.find_all(id="submission-code")
    assert len(dom) == 1
    return dom[0].text


def create_submission_url(contest: str, submission_id: str) -> str:
    return "https://atcoder.jp/contests/{}/submissions/{}".format(contest, submission_id)


def test_source_code_extractor():
    url = create_submission_url("abc213", "24866073")
    r = requests.get(url)
    if r.ok:
        s = r.text
        s = source_code_extractor(s)
        print(s)
    else:
        print("bad request: {}".format(r.reason))


test_source_code_extractor()
