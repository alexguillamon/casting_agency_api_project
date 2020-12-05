from settings import DB_PATH, TEST_DB_PATH
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.gender import Gender


db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DB_PATH if test else DB_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()


actor_movie = db.Table(
    "actor_movie",
    db.Column("actor_id", db.Integer, db.ForeignKey(
        "actors.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey(
        "movies.id"), primary_key=True),
)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    cast = db.relationship("Actor", secondary=actor_movie, backref="movies")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "cast": self.cast
        }


class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movies": self.movies
        }
