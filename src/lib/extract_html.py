from bs4 import BeautifulSoup


def source_code_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    dom = soup.find_all(id="submission-code")
    assert len(dom) == 1
    return dom[0].text


def test_source_code_extractor():
    with open("data/26320598.html") as f:
        s = f.read()
        s = source_code_extractor(s)
        print(s)


test_source_code_extractor()
