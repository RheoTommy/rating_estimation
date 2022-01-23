import pandas as pd
from tqdm import tqdm


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
    for r in tqdm(reader):
        dfi = r.query("1609588800<=epoch_second<1640962800").query("language.str.startswith('C++')", engine="python")
        df = pd.concat([df, dfi.query("contest_id.apply(@filter_with_contest_id)", engine="python")])

    print(df.head())

    df.to_csv("csv/extract.csv", index=False)


extract_csv()
