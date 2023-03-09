from flask import Flask

from app.custom_classes import MyModelView, PostAdminView
from app.extensions import admin, db, login_manager, migrate
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

    with app.app_context():
        db.create_all()

        # from app.models.admin.admin_models import User

        # user = User(name="dan", email="daniel@gmail.com", password="daniel")
        # db.session.add(user)
        # db.session.commit()
        # db.drop_all()

    return app
