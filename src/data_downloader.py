import pandas as pd
import tqdm


def sample():
    file_name = "submissions.csv"
    reader = pd.read_csv(file_name, chunksize=1000000)
    df = pd.DataFrame([])
    for r in tqdm.tqdm(reader):
        df = pd.concat([df, r.query("1609588800<=epoch_second")])
        # df = pd.concat([df, r.query("epoch_second>=1609588800").filter(like="abc")])
        # df = pd.concat([df, r.query("epoch_second>=1609588800").filter(like="arc")])
        # df = pd.concat([df, r.query("epoch_second>=1609588800").filter(like="agc")])

    print(df.head())
    print(df.shape)


sample()
