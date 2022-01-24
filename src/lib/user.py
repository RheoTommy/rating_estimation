import pickle
from datetime import datetime
from typing import Dict, List, Tuple

import requests
from tqdm import tqdm


# [(user_id, epoch_second)] -> [rating]
def get_rating(queries: List[Tuple[str, int]]) -> List[int]:
    ratings = []
    history_dict = load_all_user_histories()
    print("processing queries in \"get_rating\"")
    for (user_id, epoch_second) in tqdm(queries):
        ratings.append(get_rating_query(user_id, epoch_second, history_dict))
    return ratings


def get_rating_query(user_id: str, epoch_second: int, history_dict: Dict[str, List[Tuple[int, int]]]) -> int:
    history = history_dict[user_id]
    return get_rating_from_history(epoch_second, history)


def get_rating_from_history(epoch_second: int, history: List[Tuple[int, int]]) -> int:
    for (rating, contest_end_epoch_second) in reversed(history):
        if contest_end_epoch_second <= epoch_second:
            return rating
    raise Exception("unreachable!")


# user_id -> [(rating, end_epoch_second)]
def get_user_history(user_id: str) -> List[Tuple[int, int]]:
    url = "https://atcoder.jp/users/{}/history/json".format(user_id)
    r = requests.get(url)
    if r.ok:
        json_dist = r.json()
        res = [(0, 0)]
        for d in json_dist:
            rating = d["NewRating"]
            end_time = d["EndTime"]
            end_epoch_time = iso_time_to_epoch_second(end_time)
            res.append((rating, end_epoch_time))
        return res
    else:
        raise Exception("bad request while getting user history: {} (user_id: {})".format(r.reason, user_id))


def save_all_user_histories(user_histories: Dict[str, List[Tuple[int, int]]]):
    with open("pickle/user_histories.pickle", "wb") as f:
        pickle.dump(user_histories, f)


def load_all_user_histories() -> Dict[str, List[Tuple[int, int]]]:
    with open("pickle/user_histories.pickle", "rb") as f:
        pk = pickle.load(f)
        return pk


def iso_time_to_epoch_second(iso_time: str) -> int:
    t = datetime.fromisoformat(iso_time)
    return int(t.timestamp())
