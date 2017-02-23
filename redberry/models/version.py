import os

from redberry.models import db, RedModel
from redberry.blueprint import REDBERRY_ROOT


class RedVersion(RedModel):
    __tablename__ = 'redberry_versions'
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    @classmethod
    def last(cls):
        return cls.query.order_by('created_at DESC').first()

    @classmethod
    def all_migrations(cls):
        migrations = []

        files = os.listdir(os.path.join(REDBERRY_ROOT, 'models', 'migrations'))
        for f in files:
            try:
                bits = filter(lambda x: x is not None, f.split('_'))
                if len(bits) > 1 and int(bits[0]):
                    migrations.append(f)
            except:
                pass

        return migrations

