from sqlalchemy import event

from redberry.models import db, RedModel, generate_slug


class RedCategory(RedModel):
    __tablename__ = 'redberry_categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    @classmethod
    def sorted(cls):
        return cls.query.order_by(cls.title).all()


event.listen(RedCategory.title, 'set', generate_slug, retval=False)