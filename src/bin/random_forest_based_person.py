import os.path
import pickle

import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from pandas import Series
from sklearn.ensemble import RandomForestRegressor

import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from src.lib.submissions import load_train_data_based_person
from src.single_characteristics.analyze_characteristics import characteristics


def create_and_train_model() -> RandomForestRegressor:
    y, x = load_train_data_based_person()

    rf = RandomForestRegressor()

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )

    x_train = sum(x_train, [])
    # x_test = sum(x_test, [])
    y_train = sum(y_train, [])
    # y_test = sum(y_test, [])

    sc = StandardScaler()
    sc.fit(x_train)

    x_train = sc.transform(x_train)
    for i in range(len(x_test)):
        x_test[i] = sc.transform(x_test[i])

    rf.verbose = 1
    rf.n_jobs = -1
    rf.fit(x_train, y_train)

    xl = []
    yl = []
    ll = []
    for xt, yt in zip(x_test, y_test):
        pred_lr = rf.predict(xt)
        xl.append(Series(pred_lr).max())
        yl.append(Series(yt).max())
        ll.append(len(xt))

    i = np.argmax(ll)
    xt, yt = list(zip(x_test, y_test))[i]
    pred_lr = rf.predict(xt)
    plt.hist(pred_lr)
    plt.savefig("figs/hist.png")

    plt.clf()
    plt.cla()

    plt.scatter(pred_lr, yt)
    plt.savefig("figs/error.png")
    plt.clf()
    plt.cla()

    plt.xlabel("xl")
    plt.ylabel("yl")
    plt.scatter(xl, yl)
    plt.savefig("figs/predict_rf_based_person.png")

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
    plt.savefig("figs/rf_based_person_feature_importance.png")

    return rf


def save_model(model: RandomForestRegressor):
    with open("pickle/random_forest_based_person.pickle", "wb") as f:
        pickle.dump(model, f)


def load_model() -> RandomForestRegressor:
    with open("pickle/random_forest_based_person.pickle", "rb") as f:
        return pickle.load(f)


if os.path.exists("pickle/random_forest_based_person.pickle"):
    mdl = load_model()
else:
    mdl = create_and_train_model()
    save_model(mdl)
