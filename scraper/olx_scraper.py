# scraper/olx_scraper.py
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def scrape_links(pages=2, headless=True):
    """
    Scrape property links from OLX Pakistan search pages using Selenium.
    - pages: number of search result pages to scrape
    - headless: run browser in background (True = no GUI)
    """
    print("🔍 Starting Selenium link scraper...")
    base_url = "https://www.olx.com.pk/property-for-sale_c2"
    all_links = []
    seen = set()

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_page_load_timeout(30)

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        print(f"  Fetching page {page}: {url}")
        try:
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/item/']"))
            )
            time.sleep(2)
            link_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/item/']")
            page_links = 0
            for elem in link_elements:
                href = elem.get_attribute("href")
                if href and href.startswith("https://www.olx.com.pk/item/") and href not in seen:
                    seen.add(href)
                    all_links.append(href)
                    page_links += 1
            print(f"    ✅ Extracted {page_links} links from page {page}")
        except Exception as e:
            print(f"    ❌ Error on page {page}: {str(e)[:200]}")
            continue
        time.sleep(2)

    driver.quit()

    if all_links:
        pd.DataFrame({"Link": all_links}).to_csv("data/raw_links.csv", index=False)
        print(f"\n✅ Saved {len(all_links)} unique links to data/raw_links.csv")
        print("   First 3 links:")
        for i, link in enumerate(all_links[:3], 1):
            print(f"   {i}. {link}")
    else:
        print("\n❌ No links extracted. Try increasing pages or check selectors.")
        pd.DataFrame({"Link": []}).to_csv("data/raw_links.csv", index=False)