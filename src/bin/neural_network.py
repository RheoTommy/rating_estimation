import os.path
import random
from math import ceil

import pandas as pd
import torch
import torch.nn as nn
import  torch.nn.functional as F
from matplotlib import pyplot as plt
from tqdm import tqdm

from src.lib.data_handling import exclude_nan
from src.lib.submissions import load_all_available_submissions, Submission, get_source_codes
from src.single_characteristics.analyze_characteristics import characteristics

device = torch.device("cuda")


class Net(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, hidden_amount: int):
        super().__init__()
        self.input_layer = nn.Linear(input_size, hidden_size).to(device)
        layer = [nn.Linear(hidden_size, hidden_size).to(device) for _ in range(hidden_amount - 1)]
        self.layer = nn.ModuleList(layer)
        self.output_layer = nn.Linear(hidden_size, 1).to(device)
        self.relu = nn.ReLU().to(device)
        self.float()

    def forward(self, x):
        x = self.input_layer(x)
        x = self.relu(x)
        for l in self.layer:
            x = l(x)
            x = self.relu(x)
        x = self.output_layer(x)
        return x


def train():
    submissions = load_all_available_submissions()
    random.shuffle(submissions)
    idx = ceil(len(submissions) * 0.8)
    submissions_train = submissions[:idx]
    submissions_test = submissions[idx:]

    if os.path.isfile("pickle/nn.pickle"):
        net = torch.load("pickle/nn.pickle")
    else:
        net = Net(len(characteristics), 100, 3)

    opt = torch.optim.Adam(net.parameters(), lr=5e-4)

    epoch = 500
    batch_size = 2000
    tqdm.write("start training")
    for e in tqdm(range(epoch), desc="epoch"):
        net.train(True)
        for i in range(ceil(len(submissions_train) / batch_size)):
            subs = submissions_train[batch_size * i: min(batch_size * (i + 1), len(submissions_train))]
            source_codes = get_source_codes(subs)

            x = pd.DataFrame()
            mask = [True for _ in range(len(subs))]
            for (func, func_name, subject) in characteristics:
                features = func(tqdm(source_codes[subject], leave=False, desc="{}".format(func_name)))
                mask = list(map(lambda t: t[0] and t[1], zip(mask, exclude_nan(features))))
                x[func_name] = features
            x = x[mask]

            x = x.values.tolist()
            y = pd.Series(list(map(lambda submission: [submission.rating], subs)))
            y = y[mask].values.tolist()

            x = torch.tensor(x).to(device).float()
            y = torch.tensor(y).to(device).float()

            pre_y = net.forward(x)

            mse = nn.MSELoss()
            loss = mse(y, pre_y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            tqdm.write("loss: {}".format(loss))

        with torch.no_grad():
            source_codes = get_source_codes(submissions_test)

            x = pd.DataFrame()
            mask = [True for _ in range(len(submissions_test))]
            for (func, func_name, subject) in characteristics:
                features = func(tqdm(source_codes[subject], leave=False, desc="{}".format(func_name)))
                mask = list(map(lambda t: t[0] and t[1], zip(mask, exclude_nan(features))))
                x[func_name] = features
            x = x[mask]

            x = x.values.tolist()
            y = list(map(lambda submission: submission.rating, submissions_test))

            x = torch.tensor(x).to(device).float()
            y = torch.tensor(y).to(device).float()

            pre_y = net.forward(x)
            mse = torch.nn.MSELoss()
            loss = mse(y, pre_y)
            tqdm.write("test loss: {}".format(loss))

            plt.xlabel("pred_lr")
            plt.ylabel("y_test")
            plt.scatter(pre_y, y)
            plt.savefig("figs/predict_nn_{}.png".format(e))
            plt.cla()
            plt.clf()

    torch.save(net, "pickle/nn.pickle")


train()
