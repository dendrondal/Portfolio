import sqlite3
from click import command, option


def create_db():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Posts(
                 title TEXT NOT NULL,
                 description TEXT NOT NULL,
                 symlink TEXT NOT NULL,
                 tags TEXT NOT NULL)""")


@command()
@option('--title', prompt='Post title:')
@option('--description', prompt='Description:')
@option('--tags', prompt='Post tags:')
def add_entry(title, description, tags):
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    symlink = '/pages/{}'.format(title.lower().replace(" ", "_"))
    try:
        c.execute('INSERT INTO Posts VALUES("{}", "{}", "{}","{}")'.format(title, description, symlink, tags))
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()


def content():
    conn = sqlite3.connect('posts.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM Posts')
    return c


if __name__ == '__main__':
    add_entry()
