import os.path
import pickle
import sys
from functools import reduce

import matplotlib.pyplot as plt
import pandas
from sklearn.ensemble import RandomForestRegressor

import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from src.lib.data_handling import exclude_outliers
from src.lib.submissions import get_source_codes, load_all_available_submissions, Submission
from src.single_characteristics.analyze_characteristics import fan


def create_and_train_model() -> RandomForestRegressor:
    submissions = load_all_available_submissions()
    source_codes = get_source_codes(submissions)

    tqdm.write("preparing train data...")
    x = pd.DataFrame()
    mask = [True for _ in range(len(source_codes))]
    for (func, func_name) in fan:
        tqdm.write("processing: " + func_name)
        features = func(tqdm(source_codes))
        mask = list(map(lambda t: t[0] and t[1], zip(mask, exclude_outliers(features, 2))))
        x[func_name] = features
    x = x[mask]

    y = pd.Series(list(map(lambda submission: submission.rating, submissions)))
    y = y[mask]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    sc = StandardScaler()
    sc.fit(x_train)

    x_train = sc.transform(x_train)
    x_test = sc.transform(x_test)

    rf = RandomForestRegressor()
    rf.fit(x_train, y_train)

    pred_lr = rf.predict(x_test)

    r2_lr = r2_score(y_test, pred_lr)

    mae_lr = mean_absolute_error(y_test, pred_lr)

    print("R2 : %.3f" % r2_lr)
    print("MAE : %.3f" % mae_lr)

    plt.xlabel("pred_lr")
    plt.ylabel("y_test")
    plt.scatter(pred_lr, y_test)
    plt.savefig("figs/predict.png")

    return rf


def save_model(model: RandomForestRegressor):
    with open("pickle/random_forest.pickle", "wb") as f:
        pickle.dump(model, f)


def load_model() -> RandomForestRegressor:
    with open("pickle/random_forest.pickle", "rb") as f:
        return pickle.load(f)


def predict(model: RandomForestRegressor):
    print("input your source code here")
    source_code = reduce(lambda s, t: s + t, sys.stdin.readlines(), " ")
    x = pandas.DataFrame()
    for (func, func_name) in fan:
        features = func([source_code])
        x[func_name] = features

    y = model.predict(x)
    print(y)


if os.path.exists("pickle/random_forest.pickle"):
    mdl = load_model()
else:
    mdl = create_and_train_model()
    save_model(mdl)

predict(mdl)
