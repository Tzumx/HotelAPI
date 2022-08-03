from os import getenv
from databases import Database
from dotenv import load_dotenv
from pathlib import Path
from starlette.config import Config

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DB_USER = getenv("POSTGRES_USER", "user")
DB_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
DB_HOST = getenv("POSTGRES_SERVER", "localhost")
DB_NAME = getenv("POSTGRES_DB", "tdd")
# databases query builder
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

DB_TEST_USER = getenv("TEST_USER", "user")
DB_TEST_PASSWORD = getenv("TEST_PASSWORD", "password")
DB_TEST_HOST = getenv("TEST_SERVER", "localhost")
DB_TEST_NAME = getenv("TEST_DB", "tdd")
# test databases query builder
TEST_DB_URL = f'postgresql://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_HOST}:5432/{DB_TEST_NAME}'

config = Config()
TESTING = config('TESTING', cast=bool, default=False)
if TESTING:
    database = Database(TEST_DB_URL)
else:
    database = Database(DB_URL)
