from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.custom_classes import MyAdminIndexView

# extensions
db = SQLAlchemy()
admin = Admin(
    name="JOB SCRAPER",
    url="/admin",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),  # name="Home", template="admin/home.html", url="/admin"),
)
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
