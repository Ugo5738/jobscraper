import logging
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app import create_app
from app.main import (
    justremote_scraper,
    remote_co_scraper,
    remote_io_scraper,
    upstaff_scraper,
)

logging.basicConfig(level=logging.ERROR)

app = create_app()


def scrape():
    try:
        print("Scraping started...")
        # result1 = remote_co_scraper.scrape_remote_co()
        # print(result1)
        # time.sleep(10)
        # result2 = remote_io_scraper.scrape_remote_io()
        # print(result2)
        # time.sleep(10)
        result3 = upstaff_scraper.scrape_upstaff()
        print(result3)
        time.sleep(10)
        print("...Scraped")
        pass
    except Exception as e:
        logging.error(str(e))


scheduler = BackgroundScheduler()


if __name__ == "__main__":
    # scheduler.add_job(
    #     scrape,
    #     "interval",
    #     days=1,
    #     start_date=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
    # )
    # scheduler.start()
    scheduler.add_job(id="Scheduled scrape", func=scrape, trigger="interval", seconds=180)
    scheduler.start()
    app.run()
