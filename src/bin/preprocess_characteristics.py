import pickle
from math import ceil

import pandas as pd
from tqdm import tqdm

from src.lib.submissions import load_all_available_submissions, get_source_codes
from src.single_characteristics.analyze_characteristics import characteristics


# characteristics を変更するたびに実行しよう
def preprocess_characteristics():
    submissions = load_all_available_submissions()

    batch_size = 50000
    for i in range(ceil(len(submissions) / batch_size)):
        subs = submissions[batch_size * i:batch_size * (i + 1)]
        source_codes = get_source_codes(subs)

        x = pd.DataFrame()
        for (func, func_name, subject) in characteristics:
            features = func(tqdm(source_codes[subject], leave=False, desc=func_name))
            x[func_name] = features

        for (submission, chara) in zip(subs, x.values):
            with open("characteristics/{}.pickle".format(submission.submission_id), "wb") as f:
                pickle.dump(chara, f)


print("Make sure that these directories are exist: [characteristics]")
preprocess_characteristics()
