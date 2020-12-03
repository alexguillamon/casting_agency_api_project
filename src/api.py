from settings import ITEMS_PER_PAGE
from flask import Flask, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from database.models import db, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth


def create_app():
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request_func(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    @app.route("/")
    def index():
        return {"success": True}

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def not_found(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server failure"}
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
