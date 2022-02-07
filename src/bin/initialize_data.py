import os.path

# submissions.csv から extract.csv を作成
from src.data_preparation.create_submissions import create_submissions
from src.data_preparation.extract_csv import extract_csv
from src.data_preparation.get_source_codes import get_all_source_codes
from src.data_preparation.get_user_histories import get_all_user_histories
from src.lib.submissions import (
    load_all_submissions,
    extract_available_submissions,
    save_all_available_submissions,
)

print("Make sure that these directories exist: [csv, json, pickle, source_codes]")

if not os.path.exists("csv/extract.csv"):
    if not os.path.exists("csv/submissions.csv"):
        print("Download submissions.csv to ./csv")
        print(
            "from: https://s3-ap-northeast-1.amazonaws.com/kenkoooo/submissions.csv.gz"
        )
        exit(0)

    extract_csv()

# user_histories.pickle を作成
if not os.path.exists("pickle/user_histories.pickle"):
    get_all_user_histories()

# extract.csv から submissions.pickle を作成
if not os.path.exists("pickle/submissions.pickle"):
    if not os.path.exists("json/contests.json"):
        print("Download contests.json to ./json")
        print("from: https://kenkoooo.com/atcoder/resources/contests.json")
        exit(0)

    if not os.path.exists("json/problem-models.json"):
        print("Download problem-models.json to ./json")
        print("from: https://kenkoooo.com/atcoder/resources/problem-models.json")
        exit(0)

    create_submissions()

# source_codes/*.cpp, available_submissions.pickle を作成
if not os.path.exists("pickle/available_submissions.pickle"):
    get_all_source_codes()
    subs = load_all_submissions()
    subs = extract_available_submissions(subs)
    save_all_available_submissions(subs)
