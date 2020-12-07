from settings import ITEMS_PER_PAGE
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import db, setup_db, Movie, Actor
from database.schemas import actor_schema, movie_schema, actor_schema_partial, movie_schema_partial
from marshmallow.exceptions import ValidationError
from auth.auth import AuthError, requires_auth


def create_app(test=False):
    app = Flask(__name__)
    setup_db(app, test=test)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request_func(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # Actors Routes
    @app.route("/actors")
    def get_actors():
        page = request.args.get("page", 1, int)
        pagination = Actor.query.paginate(page=page, per_page=ITEMS_PER_PAGE)
        return {
            "success": True,
            "actors": [actor.format() for actor in pagination.items],
            "page": page,
            "page_count": pagination.pages,
            "total_actors": pagination.total
        }

    @app.route("/actors", methods=["POST"])
    def create_actor():
        data = request.get_json()
        if not data:
            abort(400)
        try:
            data = actor_schema.load(data)
        except ValidationError:
            abort(422)
        if "movies" in data:
            data["movies"] = [Movie.query.get(id) for id in data["movies"]]
            if None in data["movies"]:
                abort(404)
        actor = Actor(**data)
        res = {"success": True,
               "id": 0}
        try:
            actor.insert()
            res["id"] = actor.id
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        return res

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    def modify_actor(actor_id):
        data = request.get_json()
        if not data:
            abort(400)
        try:
            data = actor_schema_partial.load(data)
        except ValidationError:
            abort(422)
        if "movies" in data:
            data["movies"] = [Movie.query.get(id) for id in data["movies"]]
            if None in data["movies"]:
                abort(404)
        if "detach_movies" in data:
            data["detach_movies"] = [Movie.query.get(
                id) for id in data["detach_movies"]]
            if None in data["detach_movies"]:
                abort(404)

        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        res = {"success": True}
        try:
            actor.update(**data)
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        return res

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        try:
            actor.delete()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        return {"success": True}

    ####
    # Movies Routes
    ####

    @app.route("/movies")
    def get_movies():
        page = request.args.get("page", 1, int)
        pagination = Movie.query.paginate(page=page, per_page=ITEMS_PER_PAGE)
        return {
            "success": True,
            "movies": [movie.format() for movie in pagination.items],
            "page": page,
            "page_count": pagination.pages,
            "total_movies": pagination.total
        }

    @app.route("/movies", methods=["POST"])
    def create_movie():
        data = request.get_json()
        if not data:
            abort(400)
        try:
            data = movie_schema.load(data)
        except ValidationError:
            abort(422)
        if "cast" in data:
            data["cast"] = [Actor.query.get(id) for id in data["cast"]]
            if None in data["cast"]:
                abort(404)
        movie = Movie(**data)
        res = {"success": True,
               "id": 0}
        try:
            movie.insert()
            res["id"] = movie.id
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        return res

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    def modify_movie(movie_id):
        data = request.get_json()
        if not data:
            abort(400)
        try:
            data = movie_schema_partial.load(data)
        except ValidationError:
            abort(422)
        if "cast" in data:
            data["cast"] = [Actor.query.get(id) for id in data["cast"]]
            if None in data["cast"]:
                abort(404)
        if "detach_cast" in data:
            data["detach_cast"] = [Actor.query.get(
                id) for id in data["detach_cast"]]
            if None in data["detach_cast"]:
                abort(404)

        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        res = {"success": True}
        try:
            movie.update(**data)
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        return res

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        try:
            movie.delete()
        except:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        return {"success": True}

    ####
    #  Error Handlers
    ####

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400,
                     "message": "bad request"}),
            400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                     "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify(
                {"success": False, "error": 500,
                    "message": "internal server failure"}
            ),
            500,
        )

    @app.errorhandler(AuthError)
    def auth_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": error.error["code"],
                    "message": error.error["description"],
                }
            ),
            error.status_code,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
