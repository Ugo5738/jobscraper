import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app import db
from app.models.postings import posts


def scrape_remote_io():
    jobs_dict = {}
    job_description_dict = {}
    job_description_text = ""

    BASE_DIR = Path(__file__).resolve().parent.parent
    DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
    WEB_URL = "https://www.remote.io/"

    options = Options()
    # options.add_argument("--headless")
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(WEB_URL)
    # check if the blocking element exists
    try:
        blocking_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jsx-3911492254"))
        )
        # click the button to cancel the blocking element
        cancel_button = blocking_element.find_element_by_css_selector(
            "[data-modal-close-target='modal-alert-subscribe']"
        )
        cancel_button.click()
    except:
        pass
    # Find the search box
    select_element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "job-search-category"))
    )
    select_element.click()

    # Input Software Development into the search box to find related jobs
    option_element = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "option[value='software-development']"))
    )
    option_element.click()

    # Limit search to job open to anyone across the globe
    anywhere_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Anywhere')]"))
    )
    anywhere_button.click()

    # Get all the job links on that page
    job_links = []
    col_div = driver.find_element(By.CLASS_NAME, "col-span-12.space-y-4")
    elements = col_div.find_elements(
        By.XPATH, "//div[@onclick and starts-with(@onclick, 'window.location=')]"
    )
    for element in elements:
        link = element.get_attribute("onclick")
        link = link.replace("window.location='/", WEB_URL).replace("'", "")
        job_links.append(link)

    for i in range(len(job_links)):
        link = job_links[i]
        driver.get(link)

        job_title = driver.find_element(By.CSS_SELECTOR, "h1[data-rewrite='job-title']").text
        job_company_name = driver.find_element(By.CSS_SELECTOR, "p[data-rewrite='job-company-name']").text
        logo_element = driver.find_element(By.XPATH, "//div[contains(@class, 'styles_logo__1_efV')]/img")
        logo_url = logo_element.get_attribute("src")
        tag_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-rewrite='job-tags'] a")
        job_tags = [tag_element.text for tag_element in tag_elements if tag_element.text != ""]

        job_description_element = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.ID, "job-description"))
        )
        child_elements = job_description_element.find_elements(By.XPATH, "./*")

        for element in child_elements:
            if (
                element.tag_name == "h3"
                or element.tag_name == "h4"
                or element.tag_name == "p"
                or element.tag_name == "ul"
            ):
                job_description_dict[f"{element.tag_name}"] = f"{element.text}"
                job_description_text += f"{element.text} \n\n"
        location_element = job_description_element.find_element(
            By.XPATH, "//p[contains(text(),'location or timezone')]/following-sibling::div//a"
        )
        location = location_element.text

        category_element = job_description_element.find_element(
            By.XPATH, "//p[contains(text(),'category')]/following-sibling::span//a"
        )
        category = category_element.text

        posted_element = job_description_element.find_element(By.XPATH, "//li[contains(p/text(),'posted')]")
        posted_date = posted_element.text.split(" ")[0].split("\n")[-1]

        try:
            salary_element = job_description_element.find_element(
                By.XPATH, "//p[contains(text(),'yearly salary range')]/following-sibling::div"
            )
            salary_range = salary_element.text
        except:
            print("This is no salary range stated for this job")
            salary_range = ""

        post = posts.Post(
            website_name="Remote IO",
            job_title=job_title,
            job_company_name=job_company_name,
            # job_tags=job_tags,
            logo_url=logo_url,
            job_description=job_description_text,
            location=location,
            category=category,
            salary_range=salary_range,
            post_date=posted_date,
        )

        db.session.add(post)

        for job_tag in job_tags:
            tag = posts.JobTag(tag_name=job_tag)
            tag.post = post
            db.session.add(tag)

        db.session.commit()

        one_job_dict = {}
        one_job_dict["Job Title"] = job_title
        one_job_dict["Job Company Name"] = job_company_name
        one_job_dict["Job Tags"] = job_tags
        one_job_dict["Logo"] = logo_url
        one_job_dict["Location"] = location
        one_job_dict["Category"] = category
        one_job_dict["Salary Range"] = salary_range
        one_job_dict["Posted Date"] = posted_date
        one_job_dict["Job Description"] = job_description_dict

        jobs_dict[f"job_{i+1}"] = one_job_dict

        # Click on the next link, unless this is the last link in the list
        if i < len(job_links) - 1:
            next_link = job_links[i + 1]
            driver.get(next_link)
            time.sleep(2)  # Add a delay to allow the page to load

    time.sleep(5)
    driver.quit()
    # return "done"

    return jobs_dict


# print(jobs_dict)
