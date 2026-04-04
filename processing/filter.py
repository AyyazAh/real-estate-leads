# processing/filter.py
import pandas as pd
import re
import os
from utils.config import KEYWORDS
from pandas.errors import EmptyDataError

def filter_leads():
    csv_path = "data/raw_details.csv"
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print("❌ No raw data file – skipping filter.")
        return

    try:
        df = pd.read_csv(csv_path)
    except EmptyDataError:
        print("❌ raw_details.csv has no columns – skipping filter.")
        return

    if df.empty:
        print("❌ DataFrame empty – skipping filter.")
        return

    def is_valid(text):
        text = str(text).lower()
        return any(re.search(keyword, text) for keyword in KEYWORDS)

    df["Valid"] = df["Title"].apply(is_valid)
    filtered = df[df["Valid"] == True]

    # Keep all relevant columns
    all_cols = ["Title", "Description", "Price", "ImageURL", "Furnished", "Bedrooms", "Bathrooms", "Area",
                "Phone", "Seller", "ActiveAds", "Location", "Posted", "Latitude", "Longitude", "Link"]
    existing_cols = [c for c in all_cols if c in filtered.columns]
    filtered = filtered[existing_cols]

    if not filtered.empty:
        # Remove duplicates from filtered leads as well
        filtered = filtered.drop_duplicates(subset=["Seller", "Location", "Phone", "Area", "Price"], keep="first")
        filtered.to_csv("data/filtered_leads.csv", index=False)
        print(f"✅ Filtered leads saved – {len(filtered)} rows kept (duplicates removed)")
    else:
        print("⚠️ No leads matched the keywords.")
        filtered.to_csv("data/filtered_leads.csv", index=False)