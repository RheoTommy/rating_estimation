from datetime import datetime
import requests


def get_rating(user_id: str, epoch_second: int) -> int:
    history = get_user_history(user_id)
    history.reverse()
    for (rating, contest_end_epoch_second) in history:
        if contest_end_epoch_second <= epoch_second:
            return rating
    raise Exception("impossible!")


# user_id -> [(rating, end_epoch_second)]
def get_user_history(user_id: str) -> [(int, int)]:
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
        raise Exception("bad request while getting user history: {}".format(r.reason))


def iso_time_to_epoch_second(iso_time: str) -> int:
    t = datetime.fromisoformat(iso_time)
    return int(t.timestamp())


h = get_user_history("RheoTommy")
print(h)
