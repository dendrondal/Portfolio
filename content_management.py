import sqlite3
from click import command, option
import json


def create_db():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Posts(
                 title TEXT NOT NULL,
                 description TEXT NOT NULL,
                 symlink TEXT NOT NULL,
                 thumbnail TEXT NOT NULL,
                 tags TEXT NOT NULL,
                 content TEXT NOT NULL)""")


@command()
@option('--title', prompt='Post title')
@option('--description', prompt='Description')
@option('--thumb', prompt='Thumbnail image address')
@option('--tags', prompt='Post tags')
@option('--path', prompt='Path to HTML doc')
def add_entry(title, description, thumb, tags, path):
    entry = dict()
    spaceless_title = title.lower().replace(" ", "_")
    entry['title'] = title
    entry['description'] = description
    entry['symlink'] = '/blog/{}'.format(spaceless_title)
    entry['thumbnail'] = thumb
    entry['tags'] = tags
    with open(path, 'r') as rf:
        entry['content'] = rf.read()
    with open(f'./static/pages/{title}.json', 'w') as wf:
        json.dump(spaceless_title, wf)


def get_all_posts():
    with sqlite3.connect('posts.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM Posts')
        rows = c.fetchall()
        return rows


def new_post(query, var):
    with sqlite3.connect('posts.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, var)
        conn.commit()


def edit_post(query, var):
    with sqlite3.connect('posts.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, var)
        rows = c.fetchall()
        return rows


def delete_post(query, var):
    with sqlite3.connect('posts.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, var)



if __name__ == '__main__':
    add_entry()
