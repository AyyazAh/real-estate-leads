import pandas as pd

def clean_data():
    try:
        df = pd.read_csv("data/raw_details.csv")
    except:
        print("File empty — skipping cleaning ❌")
        return

    if df.empty:
        print("No data to clean ❌")
        return

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    df.to_csv("data/raw_details.csv", index=False)
    print("Data cleaned ✅")