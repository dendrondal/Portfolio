from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def content():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts')
    return c


@app.route('/')
def main_page():
    pages = [article for article in content()]
    rows = [pages[i:i + 3] for i in range(0, len(pages), 3)]
    return render_template('index.html', data=rows)


@app.route('/new-post', methods=['POST'])
def new_post():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    data = request.get_json()
    title = data['title']
    description = data['description']
    symlink = data['symlink']
    thumb = data['thumbnail']
    tags = data['tags']
    content = data['content']
    try:
        c.execute('INSERT INTO Posts VALUES(?, ?, ?, ?, ?, ?)',
                  (title, description, symlink, thumb, tags, content))
    except Exception as e:
        return e
    conn.commit()
    conn.close()
    return 'Success!'


@app.route('/blog/<post>')
def render_post(post):
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    url = f'/blog/{post}'
    c.execute('SELECT * FROM Posts WHERE symlink IS ?', (url,))
    return render_template('post.html', data=c.fetchone())


if __name__ == '__main__':
    app.run()
