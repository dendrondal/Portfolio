from flask import abort
from core import db
from models import BlogPost, PostSchema


def api_posts_read_post(title):  # noqa: E501
    """api_posts_read_post

     # noqa: E501

    :param title: Post to render.
    :type title: str

    :rtype: Post
    """
    page = BlogPost.query.filter(BlogPost.title == title)
    if page is not None:
        schema = PostSchema()
        return schema.dump(page).data
    else:
        abort(404, f'{title} not found!')


def api_posts_update_post(Payload=None):  # noqa: E501
    """api_posts_update_post

     # noqa: E501

    :param Payload: Edit existing post
    :type Payload: dict | bytes

    :rtype: None
    """
    pass


def api_posts_delete_post(title):  # noqa: E501
    """api_products_delete_post

     # noqa: E501

    :param title: Post to delete.
    :type title: str

    :rtype: None
    """
    return 'do some magic!'


def api_posts_new_post(Payload=None):  # noqa: E501
    """api_products_new_post

     # noqa: E501

    :param Payload: Create new post
    :type Payload: dict | bytes

    :rtype: None
    """
    title = Payload.get('title')
    existing_post = BlogPost.query.filter(title).one_or_none()
    if existing_post is None:
        schema = PostSchema()
        new_post = schema.load(Payload, session=db.session).data
        db.session.add(new_post)
        db.session.commit()

        return schema.dump(new_post).data, 201
    else:
        abort(409, f'{title} already exists!')


def basic_auth(username, password, required_scopes=None):
    if username == 'admin' and password == 'secret':
        return {'sub': 'admin'}
    else:
        abort(403, "Incorrect username or password")

