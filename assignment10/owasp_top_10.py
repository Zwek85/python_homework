from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the OWASP Top 10 page
url = "https://owasp.org/www-project-top-ten/"
driver.get(url)

# Give the page some time to load (optional)
driver.implicitly_wait(5)

# Find the Top 10 items
risk_elements = driver.find_elements(By.XPATH, '//a[contains(@class, "btn") and contains(@href, "/2021/")]')

top_10 = []

for elem in risk_elements[:10]:  # Only take the first 10
    title = elem.text.strip()
    link = elem.get_attribute('href').strip()
    top_10.append({"Title": title, "Link": link})

# Print the list
for item in top_10:
    print(item)

# Write to CSV
csv_path = "owasp_top_10.csv"
df = pd.DataFrame(top_10)
df.to_csv(csv_path, index=False)
print(f"\nSaved CSV to: {csv_path}")

# Cleanup
driver.quit()
