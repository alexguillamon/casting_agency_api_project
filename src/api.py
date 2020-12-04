from settings import ITEMS_PER_PAGE
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import db, setup_db, Movie, Actor
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
        pass

    @app.route("/actors", methods=["PATCH"])
    def modify_actor():
        pass

    @app.route("/actors", methods=["DELETE"])
    def delete_actor():
        pass

    # Movies Routes
    @app.route("/movies")
    def get_movies():
        pass

    @app.route("/movies", methods=["POST"])
    def create_movie():
        pass

    @app.route("/movies", methods=["PATCH"])
    def modify_movie():
        pass

    @app.route("/movies", methods=["DELETE"])
    def delete_movie():
        pass

    # Error Handlers
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
