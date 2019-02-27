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
@option('--title', prompt='Post title:')
@option('--description', prompt='Description:')
@option('--thumb', prompt='Thumbnail image address:')
@option('--tags', prompt='Post tags:')
@option('--path', prompt='Path to HTML doc:')
def add_entry(title, description, thumb, tags, path):
    entry = dict()
    entry['title'] = title
    entry['description'] = description
    entry['symlink'] = '/blog/{}'.format(title.lower().replace(" ", "_"))
    entry['thumbnail'] = thumb
    entry['tags'] = tags
    with open(path, 'r') as rf:
        entry['content'] = rf.read()
    with open(f'./static/pages/{title}.json', 'w') as wf:
        json.dump(entry, wf)


def content():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts')
    return c


if __name__ == '__main__':
    add_entry()
