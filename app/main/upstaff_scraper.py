import datetime
import os
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app import db
from app.models.postings import posts


def scrape_upstaff():
    print("started upstaff")
    jobs_dict = {}
    date_dict = {}
    job_links = []
    one_job_dict = {}
    job_description_text = ""

    BASE_DIR = Path(__file__).resolve().parent.parent
    DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
    WEB_URL = "https://up2staff.com/"

    options = Options()
    # options.add_argument("--headless")
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(WEB_URL)

    search_input = driver.find_element(By.ID, "search_keywords")
    search_input.send_keys("Full-stack programming")
    search_input.submit()

    for i in range(5):
        button = driver.find_element(By.ID, "load_more_jobs_myid")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    job_listings = soup.find("ul", class_="job_listings").find_all("li")

    for job in job_listings:
        try:
            title = job.find("div", class_="position").find("h3").text
        except:
            print("not working")

        try:
            location = job.find("div", class_="location").text.strip()
            date_str = job.find("li", class_="date").find("time").text.split()
            if "OFF: Anywhere in the World" in location and "months" not in date_str:
                link = job.find("a")["href"]
                job_links.append(link)
            date_dict[title] = date_str[0] + " " + date_str[1]
        except:
            continue

    job_links = list(set(job_links))
    for link in job_links:
        data = requests.get(link)
        soup = BeautifulSoup(data.text, "html.parser")

        title_element = soup.select_one("div.myownheaderforjob h1 a")
        title = title_element.text

        company_element = soup.select_one("div.myownheaderforjob2 div.company")
        job_company_name = company_element.select_one("strong").text
        logo_url = company_element.select_one("img.company_logo")["src"]

        category_element = soup.find(class_="job-type")
        category = category_element.text

        tags_and_content = []
        description_tags = soup.find_all("div", class_="job_description")
        for tag in description_tags:
            tag_name = tag.name
            tag_content = "\n\n".join(tag.stripped_strings)
            # tag_content = tag.stripped_strings
            #     if ">document.getElementById" in tag_content:
            #         continue
            tags_and_content.append((tag_name, tag_content))
            job_description_text += f"{tag_content} \n\n\n\n"

        # jobs_dict[title] = job_description_text

        new_post = posts.Post(
            website_name="Up2staff",
            job_title=title,
            job_company_name=job_company_name,
            # job_tags=job_tags,
            logo_url=logo_url,
            job_description=job_description_text,
            location=location,
            category=category,
            # salary_range=salary_range,
            post_date=date_dict[title],
        )

        db.session.add(new_post)
        db.session.commit()

        # one_job_dict["Job Title"] = title
        # one_job_dict["Job Company Name"] = job_company_name
        # # one_job_dict["Job Tags"] = job_tags
        # one_job_dict["Logo"] = logo_url
        # one_job_dict["Job Description"] = job_description_text
        # one_job_dict["Location"] = location
        # one_job_dict["Category"] = category
        # # one_job_dict["Salary Range"] = salary_range
        # one_job_dict["Posted Date"] = date_dict[title]

        # jobs_dict[f"job_{i+1}"] = one_job_dict

        # Click on the next link, unless this is the last link in the list
        if i < len(job_links) - 1:
            next_link = job_links[i + 1]
            driver.get(next_link)
            time.sleep(2)  # Add a delay to allow the page to load

    time.sleep(5)
    driver.quit()
    return "done"

    # return jobs_dict
