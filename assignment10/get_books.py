#Task3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# --- Setting up Selenium WebDriver ---
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Load the page ---
url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
driver.get(url)

time.sleep(3)

# --- Find all the search result <li> elements ---
search_item_class = "cp-search-result-item"
li_elements = driver.find_elements(By.CSS_SELECTOR, f"li.{search_item_class}")
print(f"Found {len(li_elements)} search results.")

# --- Initialize results list ---
results = []

# --- Loop through each result item ---
for li in li_elements:
    try:
        # Get title
        title_elem = li.find_element(By.CLASS_NAME, "cp-search-result-title")
        title = title_elem.text.strip()
    except:
        title = "N/A"

    try:
        # Get multiple authors
        author_elems = li.find_elements(By.CLASS_NAME, "cp-contributor")
        authors = "; ".join([a.text.strip() for a in author_elems])
    except:
        authors = "N/A"

    try:
        # Get format and year
        format_info_div = li.find_element(By.CLASS_NAME, "cp-format-info")
        format_year_spans = format_info_div.find_elements(By.TAG_NAME, "span")
        format_year = " ".join([s.text.strip() for s in format_year_spans if s.text.strip()])
    except:
        format_year = "N/A"

    # Add to results list
    results.append({
        "Title": title,
        "Author": authors,
        "Format-Year": format_year
    })

# --- Create DataFrame and print ---
df = pd.DataFrame(results)
print(df)

# --- Cleanup ---
driver.quit()

#Task4
import os
import json

# --- Ensure assignment10 directory exists ---
output_dir = "assignment10"
os.makedirs(output_dir, exist_ok=True)

# --- Save get_books as CSV ---
csv_path = os.path.join(output_dir, "get_books.csv")
df.to_csv(csv_path, index=False)
print(f"CSV file saved to: {csv_path}")

# --- Save get_books as JSON ---
json_path = os.path.join(output_dir, "get_books.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"JSON file saved to: {json_path}")
