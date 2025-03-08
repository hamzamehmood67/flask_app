import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Project root
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(r"instance\users.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "mykey"
