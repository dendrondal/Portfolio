from flask import render_template, request
from core import connex_app, mail_config
from core import app as flask_app
from models import BlogPost
from flask_mail import Message, Mail
import os


application = connex_app
application.add_api("swagger.yaml")


@app.route('/')
def main_page():
    pages = BlogPost.query.all()
    rows = [pages[i:i + 3] for i in range(0, len(pages), 3)]
    print(rows)
    return render_template('index.html', data=rows)


@app.route('/blog/<post>')
def render_post(post):
    page = BlogPost.query.filter(BlogPost.symlink == f'/blog/{post}').first()
    return render_template('post.html', data=page.__dict__)


@app.route('/send_email', methods=['POST'])
def send_email():
    flask_app.config.update(mail_config)
    mail = Mail(flask_app)
    sender = request.form['email']
    name = request.form['name']
    body = request.form['message']
    msg = Message(subject=f'Website inquiry from {name}',
                  sender=sender,
                  recipients=[os.environ.get('EMAIL')],
                  body=body)
    mail.send(msg)
    return "Success! Expect a response within 48 hours."


if __name__ == '__main__':
    application.run()
