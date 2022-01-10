import requests

from src.lib.extract_html import create_submission_url, source_code_extractor


def test_source_code_extractor():
    url = create_submission_url("abc213", 24866073)
    r = requests.get(url)
    if r.ok:
        s = r.text
        s = source_code_extractor(s)
        print(s)
    else:
        print("bad request: {}".format(r.reason))
