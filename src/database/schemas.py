from marshmallow import Schema, fields, validate


class ActorSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    DOB = fields.Date(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(
        ["male", "female", "other"]))
    movies = fields.List(fields.String)


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True, validate=validate.Length(min=1))
    release_date = fields.Date(required=True)
    cast = fields.List(fields.String)


actor_schema = ActorSchema()
actor_only_schema = ActorSchema(exclude=["movies"])


movie_schema = MovieSchema()
movie_only_schema = MovieSchema(exclude=["cast"])
