import os.path

import torch
import torch.nn as nn
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from src.lib.submissions import load_train_data
from src.single_characteristics.analyze_characteristics import characteristics

device = torch.device("cuda")


class Net(nn.Module):
    def __init__(self, input_size: int):
        super().__init__()
        self.relu = nn.ReLU().to(device)
        self.fc1 = nn.Linear(input_size, 128).to(device)
        self.fc2 = nn.Linear(128, 64).to(device)
        self.fc3 = nn.Linear(64, 1).to(device)
        self.dropout = nn.Dropout(p=0.5).to(device)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x


def train():
    x, y = load_train_data(make_y_list=True)

    if os.path.isfile("pickle/nn.pickle"):
        net = torch.load("pickle/nn.pickle")
    else:
        net = Net(len(characteristics))

    opt = torch.optim.Adam(net.parameters(), lr=0.001)

    epoch = 50000
    for e in tqdm(range(epoch), desc="epoch"):
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2
        )

        net.train(True)
        x_train = torch.tensor(x_train).to(device).float()
        y_train = torch.tensor(y_train).to(device).float()

        pred_y = net.forward(x_train)

        mse = nn.MSELoss()
        loss = mse(y_train, pred_y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        tqdm.write("loss: {}".format(loss))

        with torch.no_grad():
            net.eval()
            x_test = torch.tensor(x_test).to(device).float()
            y_test = torch.tensor(y_test).to(device).float()

            pred_y_test = net.forward(x_test)

            mse = nn.MSELoss()
            loss = mse(y_test, pred_y_test)

            tqdm.write("test loss: {}".format(loss))

            y_test = y_test.to("cpu").detach().numpy().copy()
            pred_y_test = pred_y_test.to("cpu").detach().numpy().copy()

            plt.xlabel("pred_lr")
            plt.ylabel("y_test")
            plt.scatter(pred_y_test, y_test)
            plt.savefig("figs/predict_nn_{}.png".format(e))
            plt.cla()
            plt.clf()

        torch.save(net, "pickle/nn.pickle")


train()
