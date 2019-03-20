from core import db, ma


class BlogPost(db.Model):
    __tablename__ = 'Posts'
    ROWID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description  = db.Column(db.String)
    symlink = db.Column(db.String)
    thumbnail = db.Column(db.String)
    tags = db.Column(db.String)
    content = db.Column(db.String)


class PostSchema(ma.ModelSchema):
    class Meta:
        model = BlogPost
        sqla_session = db.Session

