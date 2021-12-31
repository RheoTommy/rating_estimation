import collections
import json


# [(contest_id, epoch_second)] -> [during_contest?]
def is_during_contest(queries: [(int, int)]) -> [bool]:
    dc = {}

    with open("json/contests.json", "rb") as f:
        json_dist = json.load(f)
        for contest in json_dist:
            contest_id = str(contest["id"])
            end_second = int(contest["start_epoch_second"]) + int(contest["duration_second"])
            dc[contest_id] = end_second

    res = []
    for contest_id, epoch_second in queries:
        res.append(epoch_second < dc[contest_id])

    return res


# [problem_id] -> [difficulty]
def get_difficulty(queries: [str]) -> [int]:
    with open("json/problem_models.json", "rb") as f:
        json_dist = json.load(f)
        res = []
        for problem_id in queries:
            res.append(json_dist[problem_id]["difficulty"])

        return res

