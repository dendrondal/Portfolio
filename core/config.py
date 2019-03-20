from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion
from pathlib import Path


connex_app = connexion.App(__name__, specification_dir='.')
app = connex_app.app

database_uri = f'sqlite:////{Path(__file__).parents[1]}/posts.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ROOT_PATH'] = '../'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Config):
    DEVELOPMENT = False
    DEBUG = False
