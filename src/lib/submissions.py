import pickle


class Submission:
    def __init__(self, submission_id: int, epoch_second: int, problem_id: str, contest_id: str, user_id: str,
                 is_ac: bool, during_contest: bool, difficulty: int, rating: int):
        self.submission_id = submission_id
        self.epoch_second = epoch_second
        self.problem_id = problem_id
        self.contest_id = contest_id
        self.user_id = user_id
        self.is_ac = is_ac
        self.during_contest = during_contest
        self.difficulty = difficulty
        self.rating = rating


def get_all_submissions() -> [Submission]:
    path = "pickle/submissions.pickle"
    with open(path, "rb") as f:
        pk = pickle.load(f)
        return pk
