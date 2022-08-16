import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.getcwd()))
load_dotenv(verbose=True)


def get_db_env():
    return \
        os.getenv("DB_USER"),\
        os.getenv("DB_PASSWORD"),\
        os.getenv("DB_HOST"),\
        os.getenv("DB_PORT"),\
        os.getenv("DB_DATABASE")


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_LOGIN_DELTA_TIME_MINUTE = int(os.getenv("JWT_LOGIN_DELTA_TIME_MINUTE"))
JWT_REGIST_DELTA_TIME_MINUTE = int(os.getenv("JWT_REGIST_DELTA_TIME_MINUTE"))
