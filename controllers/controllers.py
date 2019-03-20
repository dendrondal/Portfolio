from flask import abort, make_response
from core import db
from models import BlogPost, PostSchema


def api_posts_read_all():
    """api_posts_read_all

    # noga: E501
    """
    posts = BlogPost.query.all()
    post_schema = PostSchema(many=True)
    data = post_schema.dump(posts).data

    return data


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


def api_posts_update_post(title, Payload=None):  # noqa: E501
    """api_posts_update_post

     # noqa: E501

    :param Payload: Edit existing post
    :type Payload: dict | bytes

    :param title: Post to update.
    :type title: str

    :rtype: None
    """
    page = BlogPost.query.filter(BlogPost.title == title).one_or_none()

    if page is not None:
        schema = BlogPost()
        update = schema.load(Payload, session=db.session).data
        update.title = page.title
        db.session.merge(update)
        db.session.commit()
        data = schema.dump(page).data

        return data, 200

    else:
        abort(404, f'{title} not found!')


def api_posts_delete_post(title):  # noqa: E501
    """api_products_delete_post

     # noqa: E501

    :param title: Post to delete.
    :type title: str

    :rtype: None
    """
    page = BlogPost.query.filter(BlogPost.title == title).one_or_none()
    if page is not None:
        db.session.delete(page)
        db.session.commit()
        return make_response(f'Deleted {title}', 200)
    else:
        abort(404, f'{title} not found!')


def api_posts_new_post(Payload=None):  # noqa: E501
    """api_products_new_post

     # noqa: E501

    :param Payload: Create new post
    :type Payload: dict | bytes

    :rtype: None
    """
    title = Payload.get('title')
    print(type(Payload), type(title))
    existing_post = BlogPost.query.filter(BlogPost.title == title).one_or_none()
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

