import lightgbm as lgb
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from src.lib.submissions import load_train_data


def train():
    x, y = load_train_data()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)

    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_eval = lgb.Dataset(x_valid, y_valid, reference=lgb_train)

    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 50,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }

    gbm = lgb.train(params, lgb_train, num_boost_round=10000, valid_sets=[lgb_train, lgb_eval],
                    early_stopping_rounds=200)

    y_pred = gbm.predict(x_test, num_iteration=gbm.best_iteration)

    scores = pd.DataFrame({'R2': r2_score(y_test, y_pred),
                           'MAE': mean_absolute_error(y_test, y_pred),
                           'MSE': mean_squared_error(y_test, y_pred),
                           'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))},
                          index=['scores'])
    print(scores)

    plt.xlabel("pred_lr")
    plt.ylabel("y_test")
    plt.scatter(y_pred, y_test, s=1)
    plt.savefig("figs/predict_gbdt.png")

    plt.cla()
    plt.clf()


train()
