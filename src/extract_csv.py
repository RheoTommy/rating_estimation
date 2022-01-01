import time

import pandas as pd
import tqdm

from lib.user import get_user_history, save_all_user_histories


def filter_with_contest_id(contest_id: str) -> bool:
    if contest_id.startswith("abc"):
        return 187 <= int(contest_id[3:])
    elif contest_id.startswith("arc"):
        return 111 <= int(contest_id[3:])
    elif contest_id.startswith("agc"):
        return 52 <= int(contest_id[3:])
    else:
        return False


def extract_csv():
    file_name = "csv/submissions.csv"
    reader = pd.read_csv(file_name, chunksize=1000000)
    df = pd.DataFrame([])
    for r in tqdm.tqdm(reader):
        dfi = r.query("1609588800<=epoch_second").query("language.str.startswith('C++')", engine="python")
        df = pd.concat([df, dfi.query("contest_id.apply(@filter_with_contest_id)", engine="python")])

    print(df.head())

    df.to_csv("csv/extract.csv", index=False)


def sort_csv():
    file_name = "csv/extract.csv"
    reader = pd.read_csv(file_name)
    reader = reader.sort_values("id", ascending=False)
    print(reader.head(70))


def get_all_user_histories():
    file_name = "csv/extract.csv"
    df = pd.read_csv(file_name)
    user_id_list = df["user_id"].unique()
    user_histories = {}
    for user_id in tqdm.tqdm(user_id_list):
        time.sleep(5)
        user_histories[user_id] = get_user_history(user_id)
    save_all_user_histories(user_histories)


# extract_csv()
# sort_csv()
get_all_user_histories()
