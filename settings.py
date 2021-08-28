import os

DB_URL = "postgres:postgres@localhost:5435/test"
# DB_URL = "postgres:postgres@db:5432/forms"
DB_STRING = os.getenv("FORMS_API_FORMS_ALCHEMY_URL", f"postgresql+psycopg2://{DB_URL}")
