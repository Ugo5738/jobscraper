import time

import click
from flask import Flask
from flask.cli import with_appcontext

from app.custom_classes import MyModelView, PostAdminView
from app.extensions import admin, db, login_manager, migrate
from app.main import (
    justremote_scraper,
    remote_co_scraper,
    remote_io_scraper,
    upstaff_scraper,
)
from app.models.admin import admin_models
from app.models.postings import posts
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return admin_models.User.query.get(int(user_id))

    # @click.command(name="scrape")
    # @with_appcontext
    # def scrape():
    #     """
    #     function to scrape remoteco, remoteio, upstaff for:
    #     - job_title
    #     - job_company_name
    #     - job_tags
    #     - job_description_dict
    #     - location
    #     - category
    #     - salary_range
    #     """

    #     print("Scrape started...")
    #     result1 = remote_co_scraper.scrape_remote_co()
    #     print(result1)
    #     time.sleep(10)
    #     result2 = remote_io_scraper.scrape_remote_io()
    #     print(result2)
    #     time.sleep(10)
    #     result3 = upstaff_scraper.scrape_upstaff()
    #     print(result3)
    #     time.sleep(10)
    #     print("...Scraped")

    # Register blueprints
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/")

    admin.add_view(
        MyModelView(
            admin_models.User,
            db.session,
            name="Admins",
            menu_icon_type="fa",
            menu_icon_value="fa-circle",
        )
    )
    admin.add_view(
        PostAdminView(
            posts.Post,
            db.session,
            name="Postings",
            menu_icon_type="fa",
            menu_icon_value="fa-database",
        )
    )
    admin.add_view(
        MyModelView(
            posts.JobTag,
            db.session,
            name="Job tags",
            menu_icon_type="fa",
            menu_icon_value="fa-database",
        )
    )

    # app.cli.add_command(scrape)

    with app.app_context():
        db.create_all()

        from app.models.admin.admin_models import User

        user = User(name="dan", email="daniel@gmail.com", password="daniel")
        db.session.add(user)
        db.session.commit()
        # db.drop_all()

    return app
