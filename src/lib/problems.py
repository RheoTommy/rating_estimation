import collections
import json


# [(contest_id, epoch_second)] -> [during_contest?]
def is_during_contest(queries: [(int, int)]) -> [bool]:
    od = collections.OrderedDict()

    with open("json/contests.json", "rb") as f:
        json_dist = json.load(f)
        for contest in json_dist:
            contest_id = str(contest["id"])
            end_second = int(contest["start_epoch_second"]) + int(contest["duration_second"])
            od[contest_id] = end_second

    res = []
    for contest_id, epoch_second in queries:
        res.append(epoch_second < od[contest_id])

    return res


# [problem_id] -> [difficulty]
def get_difficulty(queries: [str]) -> [int]:
    od = collections.OrderedDict()

    with open("json/problem_models.json", "rb") as f:
        json_dist = json.load(f)
        for key, val in json_dist.items():
            problem_id = str(key)
            difficulty = int(val["difficulty"])
            od[problem_id] = difficulty

    res = []
    for problem_id in queries:
        res.append(od[problem_id])

    return res
