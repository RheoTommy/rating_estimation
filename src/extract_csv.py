import pandas as pd
import tqdm


def extract_csv():
    file_name = "data/submissions.csv"
    reader = pd.read_csv(file_name, chunksize=1000000)
    df = pd.DataFrame([])
    for r in tqdm.tqdm(reader):
        dfi = r.query("1609588800<=epoch_second").query("language.str.startswith('C++')", engine="python")
        df = pd.concat([df, dfi.query("contest_id.str.startswith('abc')", engine="python")])
        df = pd.concat([df, dfi.query("contest_id.str.startswith('arc')", engine="python")])
        df = pd.concat([df, dfi.query("contest_id.str.startswith('agc')", engine="python")])

    print(df.head())
    print(df.shape)

    df.to_csv("data/extract.csv")


extract_csv()
