from datetime import datetime

from flask import jsonify, render_template, request, url_for
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.main import bp
from app.main.remote_co_scraper import scrape_remote_co
from app.main.remote_io_scraper import scrape_remote_io
from app.main.upstaff_scraper import scrape_upstaff
from app.models.postings import posts


@bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@bp.route("/scrape/<website_name>/<date_string>", methods=["GET", "POST"])
def scrape(website_name, date_string):
    # website_name = "Remote IO"
    # date_string = "2023-03-03"
    if website_name == "remoteio":
        web_name = "Remote IO"
    elif website_name == "remoteco":
        web_name = "Remote CO"
    elif website_name == "up2staff":
        web_name = "Up2staff"
    # date = datetime.strptime(date_string, "%Y-%m-%d")
    # print(date)

    all_post = posts.Post.query.filter_by(website_name=web_name, fill_date=date_string).all()

    post_list = []
    for post in all_post:
        post_dict = {
            "id": post.id,
            "website_name": post.website_name,
            "job_title": post.job_title,
            "job_company_name": post.job_company_name,
            "logo_url": post.logo_url,
            "job_description": post.job_description,
            "location": post.location,
            "category": post.category,
            "salary_range": post.salary_range,
            "post_date": post.post_date,
            "fill_date": post.fill_date,
            "job_tags": [tag.tag_name for tag in post.job_tags],
        }
        post_list.append(post_dict)

    return jsonify(post_list)


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
