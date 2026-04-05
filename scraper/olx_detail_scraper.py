# scraper/olx_detail_scraper.py
import time
import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

PROFILE_DIR = os.path.join(os.getcwd(), "chrome_profile")


def extract_phone_numbers(text):
    mobile = r'(?:(?:\+92|0092|0)?3[0-9]{2}[-. ]?[0-9]{7})'
    landline = r'(?:(?:0[0-9]{2,4})[-. ]?[0-9]{5,7})'
    paren = r'\(0?3[0-9]{2}\)\s*[0-9]{7}'
    plain = r'\b0?3[0-9]{2}[0-9]{7}\b'
    combined = f'({mobile}|{landline}|{paren}|{plain})'
    matches = re.findall(combined, text, re.IGNORECASE)
    numbers = []
    for m in matches:
        num = m[0] if isinstance(m, tuple) else m
        num = re.sub(r'[ \-\(\)\+]', '', num)
        num = re.sub(r'\.0$', '', num)
        if num.startswith('92') and len(num) == 12:
            num = '0' + num[2:]
        elif len(num) == 10 and num.startswith('3'):
            num = '0' + num
        numbers.append(num)
    unique = []
    for n in numbers:
        if n not in unique:
            unique.append(n)
    return ', '.join(unique) if unique else ''


def setup_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(f"user-data-dir={PROFILE_DIR}")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_page_load_timeout(30)
    return driver


def manual_login(driver):
    driver.get("https://www.olx.com.pk/")
    time.sleep(3)
    input("\n🔓 Please log in to OLX in the browser window.\n   After successful login, press Enter here to continue...")
    print("✅ Login confirmed. Continuing scraping...\n")


def scrape_details(limit=None, headless=False):
    links_path = "data/raw_links.csv"
    if not os.path.exists(links_path) or os.path.getsize(links_path) == 0:
        print("❌ raw_links.csv missing or empty – cannot scrape details.")
        return

    df = pd.read_csv(links_path)
    if df.empty or "Link" not in df.columns:
        print("❌ No links to scrape.")
        return

    links = df["Link"].tolist()
    if limit:
        links = links[:limit]

    driver = setup_driver(headless=headless)
    manual_login(driver)

    data = []
    failed = 0

    for idx, link in enumerate(links):
        print(f"  Scraping {link}")
        try:
            for attempt in range(3):
                try:
                    driver.get(link)
                    break
                except Exception as e:
                    print(f"    Retry {attempt + 1}/3: {e}")
                    time.sleep(2)
                    if attempt == 2:
                        raise
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)

            show_btn = None
            xpath = "//button[.//span[contains(text(),'Show phone number')]]"
            try:
                show_btn = driver.find_element(By.XPATH, xpath)
                if show_btn.is_displayed() and show_btn.is_enabled():
                    print("    Found button by XPath.")
            except:
                pass
            if show_btn:
                driver.execute_script("arguments[0].click();", show_btn)
                print("    Clicked 'Show phone number' button.")
                time.sleep(2)

            title = driver.title
            if " - " in title:
                title = title.split(" - ")[0]

            try:
                meta_desc = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
                description = meta_desc.get_attribute("content")
            except:
                description = ""

            price = ""
            price_selectors = [
                "span._24469da7",
                "span[aria-label*='Price']",
                "div[data-aut-id='itemPrice']",
                "span[class*='price']"
            ]
            for sel in price_selectors:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, sel)
                    price_text = price_elem.get_attribute("innerText") or price_elem.text
                    if price_text and ("Crore" in price_text or "Lac" in price_text or "Rs" in price_text):
                        price = price_text.strip()
                        break
                except:
                    continue

            image_url = ""
            try:
                img_elem = driver.find_element(By.CSS_SELECTOR, "picture source[type='image/webp']")
                image_url = img_elem.get_attribute("srcset")
                if image_url:
                    image_url = image_url.split(",")[0].strip().split(" ")[0]
            except:
                pass
            if not image_url:
                try:
                    img_elem = driver.find_element(By.CSS_SELECTOR, "div.image-gallery-slide img")
                    image_url = img_elem.get_attribute("src")
                except:
                    pass

            furnished = ""
            try:
                furnished_elem = driver.find_element(By.CSS_SELECTOR, "span._4b3efad3.a1c1940e")
                if furnished_elem and "Furnished" in furnished_elem.text:
                    furnished = "Furnished"
            except:
                pass
            if not furnished:
                try:
                    unfurnished_elem = driver.find_element(By.CSS_SELECTOR, "span._1098edef.b7af14b4")
                    if unfurnished_elem and "Unfurnished" in unfurnished_elem.text:
                        furnished = "Unfurnished"
                except:
                    pass

            bedrooms = ""
            try:
                bed_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Bed')]")
                bedrooms = bed_elem.text.strip()
            except:
                pass

            bathrooms = ""
            try:
                bath_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Bath')]")
                bathrooms = bath_elem.text.strip()
            except:
                pass

            area = ""
            area_keywords = ['Marla', 'Kanal', 'Square Feet', 'Sq. Ft', 'Sq Ft', 'Yard', 'sqft', 'sqyd']
            for keyword in area_keywords:
                try:
                    area_elem = driver.find_element(By.XPATH, f"//span[contains(text(),'{keyword}')]")
                    area = area_elem.text.strip()
                    if area:
                        break
                except:
                    continue

            seller = ""
            try:
                posted_by = driver.find_element(By.XPATH, "//span[contains(text(),'Posted by')]")
                seller_elem = posted_by.find_element(By.XPATH, "./following-sibling::div//span")
                seller = seller_elem.text.strip()
            except:
                pass

            active_ads = ""
            try:
                active_label = driver.find_element(By.XPATH, "//span[contains(text(),'Active Ads')]")
                active_elem = active_label.find_element(By.XPATH, "./following-sibling::span")
                active_ads = active_elem.text.strip()
            except:
                pass

            location = ""
            try:
                loc_elem = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Location']")
                location = loc_elem.get_attribute("innerText").strip('"')
            except:
                pass

            posted_date = ""
            try:
                date_elem = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Creation date']")
                posted_date = date_elem.text
            except:
                pass

            page_text = driver.find_element(By.TAG_NAME, "body").text
            phones = extract_phone_numbers(page_text)

            lat, lon = "", ""
            try:
                meta_geo = driver.find_element(By.CSS_SELECTOR, "meta[name='geo.position']")
                if meta_geo:
                    parts = meta_geo.get_attribute("content").split(";")
                    if len(parts) == 2:
                        lat, lon = parts[0].strip(), parts[1].strip()
            except:
                pass

            data.append({
                "Title": title,
                "Description": description,
                "Price": price,
                "ImageURL": image_url,
                "Furnished": furnished,
                "Bedrooms": bedrooms,
                "Bathrooms": bathrooms,
                "Area": area,
                "Phone": phones,
                "Seller": seller,
                "ActiveAds": active_ads,
                "Location": location,
                "Posted": posted_date,
                "Latitude": lat,
                "Longitude": lon,
                "Link": link
            })
            print(f"    ✅ Extracted: {title[:50]}... | Price: {price} | Phones: {phones if phones else 'none'}")

        except Exception as e:
            print(f"    ❌ Error: {e}")
            failed += 1

        time.sleep(0.5)

    driver.quit()

    if data:
        pd.DataFrame(data).to_csv("data/raw_details.csv", index=False)
        print(f"\n✅ Scraped {len(data)} property details ({failed} failed)")
    else:
        print(f"\n❌ No details scraped. All {failed} attempts failed.")