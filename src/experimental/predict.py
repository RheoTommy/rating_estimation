import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from src.lib.data_handling import exclude_outliers
from src.lib.submissions import with_source_codes, load_all_available_submissions
from src.single_characteristics.analyze_characteristics import fan

all_submissions = load_all_available_submissions()
dataset = with_source_codes(all_submissions)

tqdm.write("preparing train data...")
x = pd.DataFrame()
mask = [True for _ in range(len(dataset))]
for (func, func_name) in fan:
    features = func(tqdm(dataset, desc=func_name))
    mask = list(map(lambda t: t[0] and t[1], zip(mask, exclude_outliers(features, 2))))
    x[func_name] = features
x = x[mask]

y = pd.Series(list(map(lambda submission: submission.rating, all_submissions)))
y = y[mask]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

sc = StandardScaler()
sc.fit(x_train)
x_train = sc.transform(x_train)
x_test = sc.transform(x_test)

lr = LinearRegression()
lr.fit(x_train, y_train)

pred_lr = lr.predict(x_test)

r2_lr = r2_score(y_test, pred_lr)

mae_lr = mean_absolute_error(y_test, pred_lr)

print("R2 : %.3f" % r2_lr)
print("MAE : %.3f" % mae_lr)

plt.xlabel("pred_lr")
plt.ylabel("y_test")
plt.scatter(pred_lr, y_test)
plt.savefig("figs/predict.png")
