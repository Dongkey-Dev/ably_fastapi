

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

def get_db_env():
    load_dotenv(verbose=True)
    return \
        os.getenv("DB_USER"),\
        os.getenv("DB_PASSWORD"),\
        os.getenv("DB_HOST"),\
        os.getenv("DB_PORT"),\
        os.getenv("DB_DATABASE")

Base = declarative_base()
dsn = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(*get_db_env())
engine = create_engine(dsn, echo = True)
