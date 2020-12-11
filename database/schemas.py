from marshmallow import Schema, fields, validate
from marshmallow.utils import EXCLUDE


class ActorSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    DOB = fields.Date(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(
        ["male", "female", "other"]))
    movies = fields.List(fields.Int)
    detach_movies = fields.List(fields.Int)


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True, validate=validate.Length(min=1))
    release_date = fields.Date(required=True)
    cast = fields.List(fields.Int)
    detach_cast = fields.List(fields.Int)


actor_schema = ActorSchema(unknown=EXCLUDE)
actor_only_schema = ActorSchema(exclude=["movies", "detach_movies"])
actor_schema_partial = ActorSchema(unknown=EXCLUDE, partial=True)


movie_schema = MovieSchema(unknown=EXCLUDE)
movie_only_schema = MovieSchema(exclude=["cast", "detach_cast"])
movie_schema_partial = MovieSchema(unknown=EXCLUDE, partial=True)
