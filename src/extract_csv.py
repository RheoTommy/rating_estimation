import pandas as pd
import tqdm


def extract_csv():
    file_name = "csv/submissions.csv"
    reader = pd.read_csv(file_name, chunksize=1000000)
    df = pd.DataFrame([])
    for r in tqdm.tqdm(reader):
        dfi = r.query("1609588800<=epoch_second").query("language.str.startswith('C++')", engine="python")
        df = pd.concat([df, dfi.query("contest_id.str.startswith('abc')", engine="python")])
        df = pd.concat([df, dfi.query("contest_id.str.startswith('arc')", engine="python")])
        df = pd.concat([df, dfi.query("contest_id.str.startswith('agc')", engine="python")])

    print(df.head())
    print(df.shape)

    df.to_csv("csv/extract.csv", index=False)


def sort_csv():
    file_name = "csv/extract.csv"
    reader = pd.read_csv(file_name)
    reader = reader.sort_values("id", ascending=True)
    print(reader.head(100))


extract_csv()
sort_csv()
