import unittest
from api import create_app
from database.models import db, Movie, Actor
from utils.gender import Gender
from utils.db_init_data import seed


class CastingTestingCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            seed()

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

    def test_post_actors(self):
        res = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-11',
                "gender": str(Gender.male.name)
            })
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
            })
        data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

        res1 = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-30',
                "gender": "not a gender"
            })
        data1 = res1.get_json()
        self.assertEqual(res1.status_code, 422)
        self.assertFalse(data1["success"])

        res2 = self.client.post(
            "/actors", json={
                "name": '',
                "DOB": '2002-03-30',
                "gender": "not a gender"
            })
        data2 = res2.get_json()
        self.assertEqual(res2.status_code, 422)
        self.assertFalse(data2["success"])

        res3 = self.client.post(
            "/actors", json={
                "name": 'alejandro',
                "DOB": '2002-03-30',
                "gender": Gender.male.name,
                "movies": [30]
            })
        data3 = res3.get_json()
        self.assertEqual(res3.status_code, 422)
        self.assertFalse(data3["success"])

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
