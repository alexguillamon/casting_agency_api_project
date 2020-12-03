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


actor_movie = db.Table(
    "actor_movie",
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
)


class Movie(db.Model):
    pass


class Actor(db.Model):
    pass