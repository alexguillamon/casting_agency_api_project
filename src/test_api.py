import unittest
from api import create_app
from database.models import db, setup_db, Movie, Actor


class CastingTestingCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    # Actors test cases
    def test_get_actors(self):
        res = self.client.get("/actors")
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_actors_error(self):
        res = self.client.get("/actors?page=2")
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)

    # Movies test cases
    def test_get_movies(self):
        res = self.client.get("/movies")
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_get_movies_error(self):
        res = self.client.get("/movies?page=2")
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)


if __name__ == "__main__":
    unittest.main()
