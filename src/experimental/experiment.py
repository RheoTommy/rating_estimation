from src.lib.submissions import load_all_available_submissions, get_source_codes
from src.single_characteristics.analyze_characteristics import save_pair_plot, fan

all_sub = load_all_available_submissions()
users = list(map(lambda submission: submission.user_id, all_sub))
print(len(list(set(users))))

# problem_ids = ["abc189_c", "abc213_c", "abc190_c", "abc217_d", "abc213_d"]
# # problem_ids = ["arc130_b"]
#
# for problem_id in problem_ids:
#     submissions = list(
#         filter(lambda submission: submission.problem_id == problem_id, all_sub)
#     )
#     source_codes = get_source_codes(submissions)
#
#     save_pair_plot(
#         submissions, source_codes, fan, "pair_plot(problem_id={})".format(problem_id)
#     )
