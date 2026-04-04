# scripts/export_for_web.py
import pandas as pd
import json
import os
from datetime import datetime

def parse_posted_to_timestamp(posted_str):
    """Convert relative time string to actual timestamp."""
    if not posted_str or posted_str == 'Unknown':
        return datetime.now().isoformat()
    
    import re
    now = datetime.now()
    
    # Parse "X minutes ago"
    match = re.match(r'(\d+)\s*minutes?\s*ago', posted_str, re.IGNORECASE)
    if match:
        minutes = int(match.group(1))
        return (now - pd.Timedelta(minutes=minutes)).isoformat()
    
    # Parse "X hours ago"
    match = re.match(r'(\d+)\s*hours?\s*ago', posted_str, re.IGNORECASE)
    if match:
        hours = int(match.group(1))
        return (now - pd.Timedelta(hours=hours)).isoformat()
    
    # Parse "X days ago"
    match = re.match(r'(\d+)\s*days?\s*ago', posted_str, re.IGNORECASE)
    if match:
        days = int(match.group(1))
        return (now - pd.Timedelta(days=days)).isoformat()
    
    # Parse "X weeks ago"
    match = re.match(r'(\d+)\s*weeks?\s*ago', posted_str, re.IGNORECASE)
    if match:
        weeks = int(match.group(1))
        return (now - pd.Timedelta(weeks=weeks)).isoformat()
    
    # Parse "X months ago"
    match = re.match(r'(\d+)\s*months?\s*ago', posted_str, re.IGNORECASE)
    if match:
        months = int(match.group(1))
        return (now - pd.DateOffset(months=months)).isoformat()
    
    # Default to current time
    return now.isoformat()

def export_to_json():
    """Convert CSV leads to JSON format with original timestamps."""
    
    leads_file = "data/final_leads.csv"
    output_file = "data/leads_data.json"
    
    if not os.path.exists(leads_file):
        print("❌ No leads found. Run pipeline first.")
        return False
    
    df = pd.read_csv(leads_file)
    df = df.fillna('')
    
    leads = []
    for _, row in df.iterrows():
        posted_str = str(row.get('Posted', ''))
        # Store original timestamp for dynamic calculation
        original_timestamp = parse_posted_to_timestamp(posted_str)
        
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
            "PostedTimestamp": original_timestamp,  # NEW: store actual timestamp
            "ImageURL": str(row.get('ImageURL', '')),
            "Link": str(row.get('Link', ''))
        }
        leads.append(lead)
    
    data = {
        "last_updated": datetime.now().isoformat(),
        "total_leads": len(leads),
        "leads": leads
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(leads)} leads with dynamic timestamps to {output_file}")
    
    # Copy to docs folder
    import shutil
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    shutil.copy(output_file, os.path.join(docs_dir, "leads_data.json"))
    print(f"✅ Copied to {docs_dir}/leads_data.json")
    
    return True

if __name__ == "__main__":
    export_to_json()
