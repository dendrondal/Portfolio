from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion
import os


root = os.path.abspath(os.path.dirname(__file__))
connex_app = connexion.App(__name__, specification_dir='../swagger/')
app = connex_app.app

database_uri = 'sqlite:///' + os.path.join(root, 'posts.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
