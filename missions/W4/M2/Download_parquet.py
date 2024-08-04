import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setting Save Directory
save_dir = "data"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Chrome Driver
chromedriver_path = "chromedriver"

# Setting Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Setting Web Driver & Connect Website
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")

# "Expand All" 버튼 클릭
expand_button = driver.find_element(By.XPATH, "//a[contains(@href, 'javascript:expandAll();')]")
expand_button.click()
time.sleep(1)

# 2024년도 Data Extract
faq2024_section = driver.find_element(By.ID, 'faq2024')
data_links = faq2024_section.find_elements(By.XPATH, ".//a[@class='exitlink']")

# Download Data file.parquet
for link in data_links:
    file_url = link.get_attribute('href')
    if file_url.endswith('.parquet'):
        file_name = file_url.split('/')[-1]
        file_path = os.path.join(save_dir, file_name)
        
        # File Download
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"{file_name} 다운로드 완료")

# Web Driver 종료
driver.quit()

print("Success File Download")
