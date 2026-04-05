# processing/phone_extractor.py
import pandas as pd
import os
from pandas.errors import EmptyDataError

def extract_phones():
    raw_path = "data/raw_details.csv"
    filtered_path = "data/filtered_leads.csv"
    final_path = "data/final_leads.csv"

    if os.path.exists(filtered_path) and os.path.getsize(filtered_path) > 0:
        try:
            df = pd.read_csv(filtered_path)
        except EmptyDataError:
            df = pd.read_csv(raw_path) if os.path.exists(raw_path) else None
    else:
        if os.path.exists(raw_path) and os.path.getsize(raw_path) > 0:
            df = pd.read_csv(raw_path)
        else:
            print("❌ No data file found – skipping phone extraction.")
            return

    if df is None or df.empty:
        print("❌ No data to process.")
        return

    if "Phone" in df.columns:
        df["Phone"] = df["Phone"].fillna("").astype(str)
        df["Phone"] = df["Phone"].str.replace(r'\.0$', '', regex=True)
        df["Phone"] = df["Phone"].apply(lambda x: '0' + x if (len(x) == 10 and x.startswith('3')) else x)
        leads_with_phones = df[df["Phone"] != ""]
    else:
        print("⚠️ No 'Phone' column found – run the updated detail scraper first.")
        return

    if not leads_with_phones.empty:
        leads_with_phones.to_csv(final_path, index=False)
        print(f"✅ Phone numbers extracted – {len(leads_with_phones)} leads have phones.")
        print("   Sample:")
        for _, row in leads_with_phones.head(3).iterrows():
            price = row.get('Price', '')
            seller = row.get('Seller', '')
            loc = row.get('Location', '')[:30]
            print(f"   - {row['Phone']} | {price} | Seller: {seller} | {loc}")
    else:
        print("⚠️ No phone numbers found in any property.")