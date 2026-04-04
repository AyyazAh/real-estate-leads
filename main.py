# main.py
print("=== STARTING real estate lead engine ===\n")

import os
import pandas as pd
from scraper.olx_scraper import scrape_links
from scraper.olx_detail_scraper import scrape_details
from processing.filter import filter_leads
from processing.phone_extractor import extract_phones
from automation.export_leads import export_all_formats, print_leads_summary

# Step 1: Scrape fresh links
print("1. Scraping fresh property links from OLX search...")
scrape_links(pages=1, headless=True)

# Step 2: Check if we have links
links_file = "data/raw_links.csv"
if not os.path.exists(links_file):
    print("❌ No links file found. Exiting.")
    exit(1)

df_links = pd.read_csv(links_file)
if df_links.empty or "Link" not in df_links.columns:
    print("❌ raw_links.csv is empty or invalid. Exiting.")
    exit(1)

print(f"\n✅ Found {len(df_links)} links. Proceeding to scrape details...\n")

# Step 3: Scrape details
print("2. Scraping property details...")
scrape_details(limit=None, headless=False)

# Step 4: Filter leads
print("\n3. Filtering leads...")
filter_leads()

# Step 5: Extract phone numbers
print("\n4. Extracting phone numbers...")
extract_phones()

# Step 6: Export leads to CSV/Excel/HTML
print("\n5. Exporting leads...")
export_all_formats()

print("\n🚀 Pipeline completed successfully!")