from utils.gender import Gender
from database.schemas import actor_only_schema, movie_only_schema
from database import db


actor_movie = db.Table(
    "actor_movie",
    db.Column("actor_id", db.Integer, db.ForeignKey(
        "actors.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey(
        "movies.id"), primary_key=True),
)


class BaseModel(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(BaseModel):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    cast = db.relationship("Actor", secondary=actor_movie, backref="movies")

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

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "cast": [actor_only_schema.dump(actor) for actor in self.cast]
        }


class Actor(BaseModel):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)

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

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "DOB": self.DOB,
            "gender": self.gender.name,
            "movies": [movie_only_schema.dump(movie) for movie in self.movies]
        }
