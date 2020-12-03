import unittest
from api import create_app
from database.models import db, setup_db, Movie, Actor


class CastingTestingCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        setup_db(self.app, test=True)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

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


if __name__ == "__main__":
    unittest.main()
