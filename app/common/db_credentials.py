from dotenv import load_dotenv
from os import environ
load_dotenv()

db_uri = environ.get('DATABASE_URI')