from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import re

def extract_phone_numbers(text):
    mobile_pattern = r'(?:(?:\+92|0092|0)?3[0-9]{2}[-. ]?[0-9]{7})'
    landline_pattern = r'(?:(?:0[0-9]{2,4})[-. ]?[0-9]{5,7})'
    combined = f'({mobile_pattern}|{landline_pattern})'
    matches = re.findall(combined, text)
    numbers = []
    for m in matches:
        num = m[0] if isinstance(m, tuple) else m
        num = re.sub(r'[ \-]', '', num)
        if len(num) == 10 and num.startswith('3'):
            num = '0' + num
        numbers.append(num)
    return ', '.join(dict.fromkeys(numbers))

# Use a URL that previously had a phone number (e.g., the low-cost flats one)
test_url = "https://www.olx.com.pk/item/low-cost-flats-for-sale-iid-1112300574"

chrome_options = Options()
chrome_options.add_argument("--headless")  # remove to see browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(test_url)
time.sleep(3)

# Try to find and click the "Show number" button
buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-aut-id='showPhoneNumber'], button[class*='showNumber'], button[aria-label*='Show phone number']")
print(f"Found {len(buttons)} buttons")
for btn in buttons:
    print(f"Button text: {btn.text}, visible: {btn.is_displayed()}, enabled: {btn.is_enabled()}")
    if btn.is_displayed() and btn.is_enabled():
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
        print("Clicked the button")

# Get page text
page_text = driver.find_element(By.TAG_NAME, "body").text
print("Page text snippet:\n", page_text[:500])
phones = extract_phone_numbers(page_text)
print(f"Extracted phones: {phones}")

driver.quit()