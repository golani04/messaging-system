import os
from dotenv import load_dotenv


# load env variables
load_dotenv()
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
db_path = os.path.join(project_path, os.environ.get("DBNAME"))


class Config:
    DATABASE_URL = db_path
    SECRET_KEY = os.environ.get("SECRET_KEY")
