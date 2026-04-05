# main.py
import os
import pandas as pd
from datetime import datetime
from scraper.olx_scraper import scrape_links
from scraper.olx_detail_scraper import scrape_details
from processing.filter import filter_leads
from processing.phone_extractor import extract_phones

print("=== STARTING REAL ESTATE LEAD ENGINE ===\n")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================
# STEP 1: Scrape fresh property links from OLX search
# ============================================================
print("1. Scraping fresh property links from OLX search...")
print("-" * 50)
scrape_links(pages=2, headless=True)

# Check if we have links
links_file = "data/raw_links.csv"
if not os.path.exists(links_file):
    print("❌ No links file found. Exiting.")
    exit(1)

df_links = pd.read_csv(links_file)
if df_links.empty or "Link" not in df_links.columns:
    print("❌ raw_links.csv is empty or invalid. Exiting.")
    exit(1)

print(f"\n✅ Found {len(df_links)} links. Proceeding to scrape details...\n")

# ============================================================
# STEP 2: Scrape property details (title, description, price, etc.)
# ============================================================
print("2. Scraping property details...")
print("-" * 50)
scrape_details(limit=None, headless=False)

# ============================================================
# STEP 3: Filter leads by keywords
# ============================================================
print("\n3. Filtering leads...")
print("-" * 50)
filter_leads()

# ============================================================
# STEP 4: Extract phone numbers from descriptions
# ============================================================
print("\n4. Extracting phone numbers...")
print("-" * 50)
extract_phones()

# ============================================================
# STEP 5: Export data for web dashboard (with age filtering)
# ============================================================
print("\n5. Exporting data for web dashboard...")
print("-" * 50)

try:
    from scripts.export_for_web import export_to_json
    export_to_json(max_age_weeks=2)
except ImportError:
    print("⚠️ export_for_web.py not found. Skipping web export.")
except Exception as e:
    print(f"⚠️ Error during web export: {e}")

# ============================================================
# STEP 6: Display summary
# ============================================================
print("\n" + "=" * 60)
print("📊 PIPELINE SUMMARY")
print("=" * 60)

# Count leads in output files
final_file = "data/final_leads.csv"
filtered_file = "data/filtered_leads.csv"
raw_file = "data/raw_details.csv"

if os.path.exists(final_file):
    df_final = pd.read_csv(final_file)
    print(f"📞 Leads with phone numbers: {len(df_final)}")
else:
    print("📞 Leads with phone numbers: 0")

if os.path.exists(filtered_file):
    df_filtered = pd.read_csv(filtered_file)
    print(f"🔍 Filtered leads: {len(df_filtered)}")
else:
    print("🔍 Filtered leads: 0")

if os.path.exists(raw_file):
    df_raw = pd.read_csv(raw_file)
    print(f"📋 Total properties scraped: {len(df_raw)}")
else:
    print("📋 Total properties scraped: 0")

print("\n" + "=" * 60)
print(f"✅ Pipeline completed successfully at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
