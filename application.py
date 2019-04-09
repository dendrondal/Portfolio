from flask import render_template, request, send_file
from core import connex_app, mail_config
from core import app as flask_app
from models import BlogPost
from flask_mail import Message, Mail
import os


application = connex_app
application.add_api("swagger.yaml")


@application.route('/')
def main_page():
    pages = BlogPost.query.all()
    rows = [page.__dict__ for page in pages]
    return render_template('index.html', data=rows)


@application.route('/blog/<post>')
def render_post(post):
    page = BlogPost.query.filter(BlogPost.symlink == f'/blog/{post}').first()
    return render_template('post.html', data=page.__dict__)


@application.route('/send_email', methods=['POST'])
def send_email():
    print(mail_config)
    flask_app.config.update(mail_config)
    mail = Mail(flask_app)
    print(type(mail))
    sender = request.form['email']
    name = request.form['name']
    body = request.form['message']
    print(sender, body, name)
    msg = Message(subject=f'Website inquiry from {name}',
                  sender=sender,
                  recipients=[os.environ.get('EMAIL')],
                  body=body)
    mail.send(msg)
    return "Thank you for reaching out. Expect a response within 48 hours."


@application.route('/download_resume')
def download_resume():
    return send_file('static/pages/Williams_Resume.pdf',
                     as_attachment=True,
                     attachment_filename='Williams_Resume.pdf')


if __name__ == '__main__':
    application.run()
