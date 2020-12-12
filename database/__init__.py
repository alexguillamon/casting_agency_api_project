from settings import DATABASE_URL, TEST_DATABASE_URL
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app, test=False):
    db_url = TEST_DATABASE_URL if test else DATABASE_URL
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
