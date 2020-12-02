from settings import DB_PATH, TEST_DB_PATH
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH if not test else TEST_DB_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()


class Movie(db.Model):
    pass


class Actor(db.Model):
    pass