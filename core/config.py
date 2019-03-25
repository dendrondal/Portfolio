from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion
from pathlib import Path
import os

connex_app = connexion.App(__name__, specification_dir='.')
app = connex_app.app

database_uri = f'sqlite:////{Path(__file__).parents[1]}/posts.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ROOT_PATH'] = '../'

db = SQLAlchemy(app)
ma = Marshmallow(app)


mail_config = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 405,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('GMAIL'),
    "MAIL_PASSWORD": os.environ.get('GMAIL_PASS')
}
