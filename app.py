from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


@app.route('/')
def main_page():
    from .content_management import get_all_posts
    pages = get_all_posts()
    rows = [pages[i:i + 3] for i in range(0, len(pages), 3)]
    return render_template('index.html', data=rows)


@app.route('/insert', methods=['POST', 'GET'])
def new_post():
    from .content_management import get_all_posts, new_post
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        symlink = request.form['symlink']
        thumb = request.form['thumbnail']
        tags = request.form['tags']
        contents = request.form['contents']
        new_post('INSERT INTO Posts VALUES(?, ?, ?, ?, ?, ?)',
                  (title, description, symlink, thumb, tags, contents))
    results = get_all_posts()
    for result in results:
        print(result['title'])
    return render_template('crud.html', results=results)


@app.route('/blog/<post>')
def render_post(post):
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    url = f'/blog/{post}'
    c.execute('SELECT * FROM Posts WHERE symlink IS ?', (url,))
    return render_template('post.html', data=c.fetchone())


@app.route('/edit_entry', methods=['POST', 'GET'])
def edit_entry():
    from .content_management import get_all_posts, edit_post
    if request.method == 'GET':
        query_title = request.args.get('edit_title')
        editables = edit_post('SELECT * FROM Posts WHERE title IS ?', (query_title,))
    results = get_all_posts()
    return render_template('crud.html', results=results, editables=editables)


@app.route('/edit', methods=['POST', 'GET'])
def submit_edit():
    '''TODO: Add completion message to this and delete'''
    from .content_management import get_all_posts, new_post
    if request.method == 'POST':
        old_entry = request.form['old_entry']
        title = request.form['title']
        description = request.form['description']
        symlink = request.form['symlink']
        thumb = request.form['thumbnail']
        tags = request.form['tags']
        contents = request.form['contents']
        new_post('''UPDATE Posts SET title=?, description=?, symlink=?,
                  thumbnail=?, tags=?, content=? WHERE title IS ?''',
                  (title, description, symlink, thumb, tags, contents, old_entry))
        return 'Good job bro'
    results = get_all_posts()
    render_template('crud.html', results=results)


@app.route('/delete_entry', methods=['POST', 'GET'])
def delete_entry():
    from .content_management import get_all_posts, delete_post
    if request.method == 'GET':
        victim = request.args.get('del_title')
        delete_post('DELETE FROM Posts WHERE title IS ?', (victim,))
    results = get_all_posts()
    return render_template('crud.html', results=results)


if __name__ == '__main__':
    app.run()
