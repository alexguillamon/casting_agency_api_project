from dotenv import load_dotenv
import os

load_dotenv()

# Auth0 env variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS = os.getenv("ALGORITHMS")
API_AUDIENCE = os.getenv("API_AUDIENCE")

# DB env variables
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_DIALECT = os.getenv("DB_DIALECT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
# Database paths
DB_PATH = f"{DB_DIALECT}://{DB_USERNAME}@{DB_HOST}/{DB_NAME}"
TEST_DB_PATH = "sqlite:///database/testing.db"

# global pagination variable
ITEMS_PER_PAGE = 100
