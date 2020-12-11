from settings import DATABASE_URL, TEST_DATABASE_URL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.gender import Gender
from database.schemas import actor_only_schema, movie_only_schema


db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URL if test else DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


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

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "cast":
                for actor in value:
                    self.cast.append(actor)
                continue
            if key == "detach_cast":
                for actor in value:
                    self.cast.remove(actor)
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "cast": [actor_only_schema.dump(actor) for actor in self.cast]
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

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "movies":
                for movie in value:
                    self.movies.append(movie)
                continue
            if key == "detach_movies":
                for movie in value:
                    self.movies.remove(movie)
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "DOB": self.DOB,
            "gender": self.gender.name,
            "movies": [movie_only_schema.dump(movie) for movie in self.movies]
        }
