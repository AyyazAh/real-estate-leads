# scripts/export_for_web.py
import pandas as pd
import json
import os
from datetime import datetime


def export_to_json():
    """Convert CSV leads to JSON format for web dashboard."""

    leads_file = "data/final_leads.csv"
    output_file = "data/leads_data.json"

    if not os.path.exists(leads_file):
        print("❌ No leads found. Run pipeline first.")
        return False

    df = pd.read_csv(leads_file)

    # Clean data for JSON
    df = df.fillna('')

    # Convert to list of dictionaries
    leads = []
    for _, row in df.iterrows():
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
            "Posted": str(row.get('Posted', '')),
            "ImageURL": str(row.get('ImageURL', '')),
            "Link": str(row.get('Link', ''))
        }
        leads.append(lead)

    # Create data package
    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_leads": len(leads),
        "leads": leads
    }

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(leads)} leads to {output_file}")

    # Also copy to docs folder for GitHub Pages
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    # Copy JSON to docs folder
    import shutil
    shutil.copy(output_file, os.path.join(docs_dir, "leads_data.json"))
    print(f"✅ Copied to {docs_dir}/leads_data.json")

    return True


def update_github_pages():
    """Prepare files for GitHub Pages deployment."""

    # Ensure docs folder has all files
    docs_dir = "docs"

    # Copy index.html if not exists
    if not os.path.exists(os.path.join(docs_dir, "index.html")):
        print("⚠️ index.html not found in docs folder. Please create it.")

    print("\n📁 Files ready for GitHub Pages:")
    print(f"   - {docs_dir}/index.html")
    print(f"   - {docs_dir}/leads_data.json")
    print("\n🚀 To deploy:")
    print("   1. git add docs/")
    print("   2. git commit -m 'Update dashboard data'")
    print("   3. git push origin main")
    print("   4. Enable GitHub Pages in repository settings (branch: main, folder: /docs)")


if __name__ == "__main__":
    export_to_json()
    update_github_pages()