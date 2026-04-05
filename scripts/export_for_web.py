# scripts/export_for_web.py
import pandas as pd
import json
import os
import re
from datetime import datetime, timedelta


def parse_posted_to_timestamp(posted_str):
    if not posted_str or posted_str == 'Unknown' or pd.isna(posted_str):
        return datetime.now().isoformat()

    posted_str = str(posted_str).lower()
    now = datetime.now()

    match = re.match(r'(\d+)\s*minutes?\s*ago', posted_str)
    if match:
        minutes = int(match.group(1))
        return (now - timedelta(minutes=minutes)).isoformat()

    match = re.match(r'(\d+)\s*hours?\s*ago', posted_str)
    if match:
        hours = int(match.group(1))
        return (now - timedelta(hours=hours)).isoformat()

    match = re.match(r'(\d+)\s*days?\s*ago', posted_str)
    if match:
        days = int(match.group(1))
        return (now - timedelta(days=days)).isoformat()

    match = re.match(r'(\d+)\s*weeks?\s*ago', posted_str)
    if match:
        weeks = int(match.group(1))
        return (now - timedelta(weeks=weeks)).isoformat()

    match = re.match(r'(\d+)\s*months?\s*ago', posted_str)
    if match:
        months = int(match.group(1))
        return (now - timedelta(days=months * 30)).isoformat()

    return now.isoformat()


def is_older_than_weeks(timestamp_str, weeks=2):
    try:
        posted_date = datetime.fromisoformat(timestamp_str)
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        return posted_date < cutoff_date
    except:
        return False


def export_to_json(max_age_weeks=2):
    leads_file = "data/final_leads.csv"
    output_file = "data/leads_data.json"

    if not os.path.exists(leads_file):
        print(f"❌ No leads found at {leads_file}")
        return False

    df = pd.read_csv(leads_file)
    df = df.fillna('')

    print(f"📊 Processing {len(df)} leads...")

    leads = []
    removed_count = 0

    for _, row in df.iterrows():
        posted_str = str(row.get('Posted', ''))
        original_timestamp = parse_posted_to_timestamp(posted_str)

        if is_older_than_weeks(original_timestamp, max_age_weeks):
            removed_count += 1
            continue

        lead = {
            "Title": str(row.get('Title', '')),
            "Price": str(row.get('Price', '')),
            "Phone": str(row.get('Phone', '')),
            "Location": str(row.get('Location', '')),
            "Seller": str(row.get('Seller', '')),
            "Furnished": str(row.get('Furnished', '')),
            "Area": str(row.get('Area', '')),
            "Bedrooms": str(row.get('Bedrooms', '')),
            "Bathrooms": str(row.get('Bathrooms', '')),
            "Posted": posted_str,
            "PostedTimestamp": original_timestamp,
            "ImageURL": str(row.get('ImageURL', '')),
            "Link": str(row.get('Link', ''))
        }
        leads.append(lead)

    data = {
        "last_updated": datetime.now().isoformat(),
        "total_leads": len(leads),
        "removed_old": removed_count,
        "max_age_weeks": max_age_weeks,
        "leads": leads
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(leads)} leads (removed {removed_count} ads older than {max_age_weeks} weeks)")

    import shutil
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    shutil.copy(output_file, os.path.join(docs_dir, "leads_data.json"))
    print(f"✅ Copied to {docs_dir}/leads_data.json")

    return True


if __name__ == "__main__":
    export_to_json(max_age_weeks=2)