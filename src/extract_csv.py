import pandas as pd
import tqdm


def filter_with_contest_id(contest_id: str) -> bool:
    if contest_id.startswith("abc"):
        return 187 <= int(contest_id[3:])
    elif contest_id.startswith("arc"):
        return 111 <= int(contest_id[3:])
    elif contest_id.startswith("agc"):
        return 52 <= int(contest_id[3:])
    else:
        return False


def extract_csv():
    file_name = "csv/submissions.csv"
    reader = pd.read_csv(file_name, chunksize=1000000)
    df = pd.DataFrame([])
    for r in tqdm.tqdm(reader):
        dfi = r.query("1609588800<=epoch_second").query("language.str.startswith('C++')", engine="python")
        df = pd.concat([df, dfi.query("contest_id.apply(@filter_with_contest_id)", engine="python")])

    print(df.head())

    df.to_csv("csv/extract.csv", index=False)


def sort_csv():
    file_name = "csv/extract.csv"
    reader = pd.read_csv(file_name)
    reader = reader.sort_values("id", ascending=False)
    print(reader.head(70))


def unique_user():
    file_name = "csv/extract.csv"
    df = pd.read_csv(file_name)
    print("all submission count: {}".format(df.shape[0]))
    print("unique user count: {}".format(df["user_id"].nunique()))


# extract_csv()
# sort_csv()
unique_user()
