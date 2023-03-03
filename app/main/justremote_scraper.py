import datetime
import os
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# BASE_DIR = Path(__file__).resolve().parent.parent
# DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
# WEB_URL = "https://justremote.co/remote-developer-jobs"

# options = Options()
# # options.add_argument("--headless")
# service = Service(DRIVER_PATH)
# driver = webdriver.Chrome(service=service, options=options)
# driver.get(WEB_URL)

# remote_jobs_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Remote Jobs')]"))
# )
# remote_jobs_button.click()

# developer_button = driver.find_element(By.LINK_TEXT, "Developer")
# developer_button.click()

# time.sleep(5)
# driver.quit()
