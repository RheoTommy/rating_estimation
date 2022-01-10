import time

from tqdm import tqdm

from src.lib.extract_html import get_source_code
from src.lib.submissions import load_all_submissions, extract_available_submissions, save_all_available_submissions


def get_all_source_codes():
    submissions = load_all_submissions()
    for submission in tqdm(submissions):
        for _ in range(5):
            try:
                time.sleep(0.1)
                source_code = get_source_code(submission.contest_id, submission.submission_id)
                with open("source_codes/{}.cpp".format(submission.submission_id), "wb") as f:
                    f.write(source_code.encode())
            except Exception as e:
                print(e)
            else:
                break


get_all_source_codes()
subs = load_all_submissions()
subs = extract_available_submissions(subs)
save_all_available_submissions(subs)
