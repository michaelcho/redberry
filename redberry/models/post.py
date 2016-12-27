from sqlalchemy import event

from redberry.models import db, RedModel, generate_slug


categories_posts = db.Table('redberry_categories_posts',
                              db.Column('category_id', db.Integer, db.ForeignKey('redberry_categories.id'), nullable=False),
                              db.Column('post_id', db.Integer, db.ForeignKey('redberry_posts.id'), nullable=False),
                              db.PrimaryKeyConstraint('category_id', 'post_id'))


class RedPost(RedModel):
    __tablename__ = 'redberry_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    content = db.Column(db.Text)
    published = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    categories = db.relationship("RedCategory", secondary=categories_posts, backref='posts')

    @classmethod
    def all_published(cls):
        return cls.query.filter_by(published=True).order_by('created_at DESC').all()


event.listen(RedPost.title, 'set', generate_slug, retval=False)
