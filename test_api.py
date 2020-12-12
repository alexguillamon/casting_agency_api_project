from settings import ASSISTANT_TOKEN, DIRECTOR_TOKEN, PRODUCER_TOKEN
import unittest
from api import create_app
from database import db
from database.models import Movie, Actor
from utils.gender import Gender
from utils.db_init_data import seed


class inheritedTestCase(unittest.TestCase):
    header = {"Content-Type": "application/json",
              "Authorization": f"Bearer {PRODUCER_TOKEN}"}
    assistant_header = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {ASSISTANT_TOKEN}"}
    director_header = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {DIRECTOR_TOKEN}"}
    producer_header = {"Content-Type": "application/json",
                       "Authorization": f"Bearer {PRODUCER_TOKEN}"}

    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            seed()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def check_success(self, code, data, expected_code=200):
        """
        This method abstract assertions for successfull status codes
        and `success`from JSON data.

        Parameters:
            code: status code from the request
            data: JSON parsed data from the request
            expected_code: the expected code from the request
        """
        self.assertEqual(code, expected_code)
        self.assertTrue(data["success"])
        return True

    def check_failure(self, code, data, expected_code):
        """
        This method abstract assertions for unsuccessfull status codes
        and `success` from JSON data.

        Parameters:
            code: status code from the request
            data: JSON parsed data from the request
            expected_code: the expected code from the request
        """
        self.assertEqual(code, expected_code)
        self.assertEqual(data["error"], expected_code)
        return True

    def client_request(self, path, options=None):
        """
        This method abstracts client request code.

        Parameters:
            path: path to the desired endpoint
            options: dictionary of parameters to be passed to the test client
                    This dictionary will allow any parameter that
                    flask.testing.FlaskClient's `open` method takes.
                    For reference see https://flask.palletsprojects.com/en/1.1.x/api/#flask.testing.FlaskClient
        """
        if options is None:
            options = {
                "method": "GET",
                "json": {},
                "headers": self.header
            }
        res = self.client.open(path, **options)
        data = res.get_json()
        return [res.status_code, data]


class ActorsTestingCase(inheritedTestCase):
    endpoint = "/actors"

    def test_get_actors(self):
        code, data = self.client_request(self.endpoint)
        self.check_success(code, data, 200)

    def test_get_actors_error(self):
        path = self.endpoint + "?page=2"
        code, data = self.client_request(path)
        self.check_failure(code, data, 404)

    def test_post_actors(self):
        res = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-11',
                "gender": str(Gender.male.name)
            }, headers=self.header)
        data = res.get_json()

        with self.app.app_context():
            actor = Actor.query.filter_by(name="alejandro").first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], actor.id)

    def test_post_actors_error(self):
        res = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-33',
                "gender": Gender.male.name
            }, headers=self.header)
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

        res1 = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-30',
                "gender": "not a gender"
            }, headers=self.header)
        data1 = res1.get_json()
        self.assertEqual(res1.status_code, 422)
        self.assertFalse(data1["success"])

        res2 = self.client.post(
            "/actors", json={
                "name": '',
                "DOB": '2002-03-30',
                "gender": "not a gender"
            }, headers=self.header)
        data2 = res2.get_json()
        self.assertEqual(res2.status_code, 422)
        self.assertFalse(data2["success"])

        res3 = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-30',
                "gender": Gender.male.name,
                "movies": [30]
            }, headers=self.header)
        data3 = res3.get_json()
        self.assertEqual(res3.status_code, 404)
        self.assertFalse(data3["success"])

    def test_patch_actor(self):
        res = self.client.patch("/actors/1", json={
            "name": "New Name",
            "movies": [2, 3],
            "detach_movies": [1]
        }, headers=self.header)
        data = res.get_json()
        with self.app.app_context():
            actor = Actor.query.get(1)
            movies = actor.movies

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(actor.name, "New Name")
        self.assertEqual(len(movies), 2)

    def test_patch_actor_error(self):
        res = self.client.patch("/actors/1", json={
            "name": "",
            "movies": [2, 3],
            "detach_movies": [1]
        }, headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

        res = self.client.patch("/actors/1", json={
            "name": "New Name",
            "movies": [2, 3, 20],
            "detach_movies": [1]
        }, headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

        res = self.client.patch("/actors/1", json={
            "name": "New Name",
            "movies": [2, 3],
            "detach_movies": [60]
        }, headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_delete_actor(self):
        res = self.client.delete("/actors/1", headers=self.header)
        data = res.get_json()

        with self.app.app_context():
            actor = Actor.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(actor)

    def test_delete_actor_error(self):
        res = self.client.delete("/actors/40", headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])


class MoviesTestingCase(inheritedTestCase):

    def test_get_movies(self):
        res = self.client.get("/movies", headers=self.header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_movies_error(self):
        res = self.client.get("/movies?page=2", headers=self.header)
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)

    def test_post_movie(self):
        res = self.client.post(
            "/movies", json={
                "title": "The day before yesterday",
                "release_date": '2021-03-11',
            }, headers=self.header)
        data = res.get_json()

        with self.app.app_context():
            movie = Movie.query.filter_by(
                title="The day before yesterday").first()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["id"], movie.id)

    def test_post_movie_error(self):
        res = self.client.post(
            "/movies", json={
                "title": '',
                "release_date": '2002-03-01',
            }, headers=self.header)
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

        res1 = self.client.post(
            "/movies", json={
                "title": 'Title',
                "release_date": '2002-03-33',
            }, headers=self.header)
        data1 = res1.get_json()
        self.assertEqual(res1.status_code, 422)
        self.assertFalse(data1["success"])

        res2 = self.client.post(
            "/movies", json={
                "title": 'Title',
                "release_date": '2002-03-30',
                "cast": [35, 50, 3]
            }, headers=self.header)
        data2 = res2.get_json()
        self.assertEqual(res2.status_code, 404)
        self.assertFalse(data2["success"])

    def test_patch_movie(self):
        res = self.client.patch("/movies/1", json={
            "title": "New Name",
            "cast": [2, 3],
            "detach_cast": [1]
        }, headers=self.header)
        data = res.get_json()
        with self.app.app_context():
            movie = Movie.query.get(1)
            cast = movie.cast

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(movie.title, "New Name")
        self.assertEqual(len(cast), 2)

    def test_patch_movie_error(self):
        res = self.client.patch("/movies/1", json={
            "title": "",
            "cast": [2, 3],
            "detach_cast": [1]
        }, headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

        res = self.client.patch("/movies/1", json={
            "title": "New Name",
            "cast": [2, 3, 20],
            "detach_cast": [1]
        }, headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

        res = self.client.patch("/movies/1", json={
            "title": "New Name",
            "cast": [2, 3],
            "detach_cast": [60]
        }, headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_delete_movie(self):
        res = self.client.delete("/movies/1", headers=self.header)
        data = res.get_json()

        with self.app.app_context():
            movie = Movie.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIsNone(movie)

    def test_delete_movie_error(self):
        res = self.client.delete("/movies/40", headers=self.header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])


class RolesTestingCase(inheritedTestCase):
    def test_assistant_role(self):
        res = self.client.get("/actors", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        res = self.client.get("/movies", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_assistant_role_error(self):
        res = self.client.post("/actors", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

        res = self.client.post("/movies", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

        res = self.client.patch("/actors/1", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

        res = self.client.patch("/movies/1", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

        res = self.client.delete("/actors/1", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

        res = self.client.delete("/movies/1", headers=self.assistant_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

    def test_director_role(self):
        res = self.client.get("/actors", headers=self.director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        res = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-11',
                "gender": str(Gender.male.name)
            }, headers=self.director_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        res = self.client.patch("/actors/1", json={
            "name": "New Name",
            "movies": [2, 3],
            "detach_movies": [1]
        }, headers=self.director_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        res = self.client.delete("/actors/1", headers=self.director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        res = self.client.get("/movies", headers=self.director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

        res = self.client.patch("/movies/1", json={
            "title": "New Name",
            "cast": [2, 3],
            "detach_cast": []
        }, headers=self.director_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_director_role_error(self):
        res = self.client.post(
            "/movies", json={
                "title": "The day before yesterday",
                "release_date": '2021-03-11',
            }, headers=self.director_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])

        res = self.client.delete("/movies/1", headers=self.director_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data["success"])


if __name__ == "__main__":
    unittest.main()
