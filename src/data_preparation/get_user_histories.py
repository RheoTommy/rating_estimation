import pandas as pd
import tqdm
import time

from src.lib.user import get_user_history, save_all_user_histories, load_all_user_histories


def get_all_user_histories():
    file_name = "csv/extract.csv"
    df = pd.read_csv(file_name)
    user_id_list = df["user_id"].unique()
    user_histories = load_all_user_histories()
    for user_id in tqdm.tqdm(user_id_list):
        while user_id in user_histories:
            try:
                time.sleep(0.5)
                user_histories[user_id] = get_user_history(user_id)
            except Exception as e:
                print(e)
            else:
                break
    save_all_user_histories(user_histories)


get_all_user_histories()
