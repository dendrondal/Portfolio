from flask import render_template, request, send_file
from flask_frozen import Freezer
from flask_mail import Message, Mail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_flatpages import FlatPages
import connexion
from pathlib import Path
import sys

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
pages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
def main_page():
    print([page.meta for page in pages])
    return render_template('index.html', pages=pages)


@app.route('/<path:path>/')
def render_post(path):
    page = pages.get_or_404(path)
    return render_template('post.html', page=page)


@app.route('/intro/')
def intro():
    return render_template('intro.html')


@app.route('/download_resume')
def download_resume():
    return send_file('Williams_Resume.pdf',
                     as_attachment=True,
                     attachment_filename='Williams_Resume.pdf')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run()