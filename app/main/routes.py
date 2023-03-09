import threading
import time
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app, jsonify, render_template, request, url_for

from app.extensions import db
from app.main import bp, remote_co_scraper, remote_io_scraper, upstaff_scraper
from app.models.admin import admin_models
from app.models.postings import posts


@bp.route("/get-scraped/<website_name>", methods=["GET", "POST"])
def get_scraped(website_name):
    if website_name == "remoteio":
        web_name = "Remote IO"
    elif website_name == "remoteco":
        web_name = "Remote CO"
    elif website_name == "up2staff":
        web_name = "Up2staff"

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")

    all_post = posts.Post.query.filter_by(website_name=web_name, fill_date=date).all()

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
            "post_time": post.post_time,
            "fill_date": post.fill_date,
            "job_tags": [tag.tag_name for tag in post.job_tags],
        }
        post_list.append(post_dict)

    return jsonify(post_list)


@bp.route("/scrape/<website_name>", methods=["GET", "POST"])
def scrape(website_name):
    if website_name == "remoteio":
        remote_io_scraper.scrape_remote_io()
    elif website_name == "remoteco":
        remote_co_scraper.scrape_remote_co()
    elif website_name == "up2staff":
        upstaff_scraper.scrape_upstaff()

    return "Done scraping"


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
