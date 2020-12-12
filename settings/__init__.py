from dotenv import load_dotenv
import os

if os.path.isfile(".env"):
    load_dotenv()

# Auth0 env variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS = os.getenv("ALGORITHMS")
API_AUDIENCE = os.getenv("API_AUDIENCE")

# Database paths
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = "sqlite:///database/testing.db"
# Testing Tokens
ASSISTANT_TOKEN = os.getenv("ASSISTANT_TOKEN")
DIRECTOR_TOKEN = os.getenv("DIRECTOR_TOKEN")
PRODUCER_TOKEN = os.getenv("PRODUCER_TOKEN")


# global pagination variable
ITEMS_PER_PAGE = 100
