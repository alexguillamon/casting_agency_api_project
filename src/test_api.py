import unittest
import json
from flask_sqlalchemy import SQLAlchemy
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

    def test_dummy(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
