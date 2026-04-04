# upload_to_gist.py
import requests
import pandas as pd
import json
import os
from datetime import datetime

# GitHub configuration
GITHUB_TOKEN = ""  # Your GitHub token (will be prompted first time)
GIST_ID = ""  # Your gist ID (will be created automatically)


def get_credentials():
    """Get GitHub token from user or environment."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = input("🔑 Enter your GitHub Personal Access Token: ").strip()
        save = input("Save token for future use? (y/n): ").strip().lower()
        if save == 'y':
            with open("github_token.txt", "w") as f:
                f.write(token)
            print("✅ Token saved to github_token.txt")
    return token


def create_gist(token, filename="leads.json"):
    """Create a new gist if one doesn't exist."""
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "description": "Real Estate Leads - Auto-updated daily",
        "public": True,
        "files": {
            filename: {
                "content": json.dumps({"message": "Initializing..."}, indent=2)
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        gist_data = response.json()
        gist_id = gist_data['id']
        gist_url = gist_data['html_url']
        raw_url = gist_data['files'][filename]['raw_url']

        print(f"✅ Gist created!")
        print(f"   ID: {gist_id}")
        print(f"   URL: {gist_url}")
        print(f"   Raw URL: {raw_url}")

        # Save gist info
        with open("gist_info.json", "w") as f:
            json.dump({"gist_id": gist_id, "raw_url": raw_url}, f)

        return gist_id, raw_url
    else:
        print(f"❌ Failed to create gist: {response.status_code}")
        print(response.text)
        return None, None


def get_gist_info():
    """Load gist info from file."""
    if os.path.exists("gist_info.json"):
        with open("gist_info.json", "r") as f:
            return json.load(f)
    return None


def update_gist(token, gist_id, data):
    """Update existing gist with new data."""
    url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    files = {
        "leads.json": {
            "content": json.dumps(data, indent=2, default=str)
        }
    }

    response = requests.patch(url, headers=headers, json={"files": files})

    if response.status_code == 200:
        print("✅ Gist updated successfully!")
        return True
    else:
        print(f"❌ Failed to update gist: {response.status_code}")
        print(response.text)
        return False


def upload_leads_to_gist():
    """Upload leads data to GitHub Gist."""

    # Read leads
    leads_file = "data/final_leads.csv"
    if not os.path.exists(leads_file):
        print("❌ No leads found. Run the pipeline first.")
        return None

    df = pd.read_csv(leads_file)
    if df.empty:
        print("❌ No leads to upload.")
        return None

    # Get token
    token = get_credentials()
    if not token:
        print("❌ No GitHub token provided.")
        return None

    # Get or create gist
    gist_info = get_gist_info()
    if gist_info and 'gist_id' in gist_info:
        gist_id = gist_info['gist_id']
        raw_url = gist_info['raw_url']
        print(f"📁 Using existing gist: {gist_id}")
    else:
        gist_id, raw_url = create_gist(token)
        if not gist_id:
            return None

    # Prepare data
    leads_data = {
        "last_updated": datetime.now().isoformat(),
        "total_leads": len(df),
        "with_phone": len(df[df['Phone'].notna() & (df['Phone'] != '')]),
        "unique_locations": df['Location'].nunique(),
        "furnished_count": len(df[df['Furnished'] == 'Furnished']),
        "recent_count": len(df[df['Posted'].str.contains('hour|minute', na=False)]),
        "leads": df.to_dict('records')
    }

    # Upload
    success = update_gist(token, gist_id, leads_data)

    if success:
        print(f"\n🌐 Public Dashboard URL:")
        print(f"   https://gist.githubusercontent.com/raw/{gist_id}/leads.json")
        print(f"\n📊 Use this URL in your public HTML dashboard.")

    return raw_url


def upload_summary_only():
    """Upload only summary statistics (lighter, more private)."""

    leads_file = "data/final_leads.csv"
    if not os.path.exists(leads_file):
        print("❌ No leads found.")
        return None

    df = pd.read_csv(leads_file)

    # Create summary (no personal phone numbers)
    summary = {
        "last_updated": datetime.now().isoformat(),
        "total_leads": len(df),
        "with_phone": len(df[df['Phone'].notna() & (df['Phone'] != '')]),
        "unique_locations": df['Location'].nunique(),
        "furnished_count": len(df[df['Furnished'] == 'Furnished']),
        "average_price": "N/A",  # You can calculate if needed
        "top_locations": df['Location'].value_counts().head(5).to_dict(),
        "top_sellers": df['Seller'].value_counts().head(5).to_dict()
    }

    # Get token and gist (same as above)
    token = get_credentials()
    if not token:
        return None

    gist_info = get_gist_info()
    if gist_info:
        gist_id = gist_info['gist_id']
    else:
        gist_id, _ = create_gist(token, "summary.json")
        if not gist_id:
            return None

    url = f"https://api.github.com/gists/{gist_id}"
    headers = {"Authorization": f"token {token}"}

    files = {"summary.json": {"content": json.dumps(summary, indent=2, default=str)}}

    response = requests.patch(url, headers=headers, json={"files": files})

    if response.status_code == 200:
        print("✅ Summary uploaded (no phone numbers included)")
        return True
    return False


if __name__ == "__main__":
    upload_leads_to_gist()