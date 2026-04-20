import os

class Config:
    SECRET_KEY = "secret123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///library.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'templates')
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static')