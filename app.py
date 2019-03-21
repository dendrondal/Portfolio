from flask import render_template, request
from core.config import connex_app
from models import BlogPost


app = connex_app
app.add_api("swagger.yaml")


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



if __name__ == '__main__':
    app.run()
