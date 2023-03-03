# import os
# import time
# from pathlib import Path

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

# BASE_DIR = Path(__file__).resolve().parent.parent
# DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
# WEB_URL = "https://up2staff.com/qa-engineer-at-close"

# options = Options()
# # options.add_argument("--headless")
# service = Service(DRIVER_PATH)
# driver = webdriver.Chrome(service=service, options=options)

# driver.get(WEB_URL)

# title_element = driver.find_element(By.XPATH, "//div[@class='myownheaderforjob']/h1/a")
# title_text = title_element.text


# company_element = driver.find_element(By.XPATH, "//div[@class='myownheaderforjob2']//div[@class='company']")
# company_name = company_element.find_element(By.TAG_NAME, "strong").text
# company_logo_url = company_element.find_element(By.CSS_SELECTOR, "img.company_logo").get_attribute("src")

# category_element = driver.find_element(By.CLASS_NAME, "job-type")
# category = category_element.text

# job_description_elements = driver.find_element(By.CLASS_NAME, "job_description")
# tags_and_content = []
# for tag in job_description_elements.find_elements(By.XPATH, "./*"):
#     tag_name = tag.tag_name
#     tag_content = tag.get_attribute("innerHTML")
#     tags_and_content.append((tag_name, tag_content))
# for tag, content in tags_and_content:
#     if ">document.getElementById" in content:
#         continue
