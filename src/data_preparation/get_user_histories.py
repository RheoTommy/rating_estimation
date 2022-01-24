import pandas as pd
from tqdm import tqdm
import time

from src.lib.user import (
    get_user_history,
    save_all_user_histories,
    load_all_user_histories,
)


def get_all_user_histories():
    file_name = "csv/extract.csv"
    df = pd.read_csv(file_name)
    user_id_list = df["user_id"].unique()
    user_histories = load_all_user_histories()
    for user_id in tqdm(user_id_list):
        if user_id in user_histories:
            continue
        while True:
            try:
                time.sleep(0.5)
                user_histories[user_id] = get_user_history(user_id)
            except Exception as e:
                tqdm.write(e)
            else:
                break
    save_all_user_histories(user_histories)


get_all_user_histories()
