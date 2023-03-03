import os

from dotenv import load_dotenv

load_dotenv()


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///" + os.path.join(BASEDIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "kleinuduh@gmail.com"
    MAIL_PASSWORD = os.environ.get("FLASK_MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
