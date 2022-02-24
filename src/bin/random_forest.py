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

from src.lib.submissions import load_train_data
from src.single_characteristics.analyze_characteristics import characteristics


def create_and_train_model() -> RandomForestRegressor:
    x, y = load_train_data()

    rf = RandomForestRegressor()

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )

    sc = StandardScaler()
    sc.fit(x_train)

    x_train = sc.transform(x_train)
    x_test = sc.transform(x_test)

    rf.verbose = 1
    rf.n_jobs = -1
    rf.fit(x_train, y_train)

    pred_lr = rf.predict(x_test)

    r2_lr = r2_score(y_test, pred_lr)

    mae_lr = mean_absolute_error(y_test, pred_lr)

    tqdm.write("R2 : %.3f" % r2_lr)
    tqdm.write("MAE : %.3f" % mae_lr)

    plt.xlabel("pred_lr")
    plt.ylabel("y_test")
    plt.scatter(pred_lr, y_test, s=4)
    plt.savefig("figs/predict_rf.png")

    plt.cla()
    plt.clf()

    forest_importance = pd.Series(
        rf.feature_importances_, index=list(map(lambda t: t[1], characteristics))
    )

    fig, ax = plt.subplots()
    forest_importance.plot.bar(ax=ax)
    ax.set_title("Feature importance using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    plt.tight_layout()
    plt.savefig("figs/rf_feature_importance.png")

    return rf


def save_model(model: RandomForestRegressor):
    with open("pickle/random_forest.pickle", "wb") as f:
        pickle.dump(model, f)


def load_model() -> RandomForestRegressor:
    with open("pickle/random_forest.pickle", "rb") as f:
        return pickle.load(f)


if os.path.exists("pickle/random_forest.pickle"):
    mdl = load_model()
else:
    mdl = create_and_train_model()
    save_model(mdl)
