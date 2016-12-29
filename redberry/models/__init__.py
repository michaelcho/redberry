from slugify import slugify
from html5lib_truncation import truncate_html

from redberry.blueprint import cms

db = cms.config['db']


def generate_slug(target, value, oldvalue, initiator):
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value)


class RedModel(db.Model):
    """
    All Redberry models inherit from this base class. It adds Django-like save() and delete() methods.
    """
    __abstract__ = True

    @staticmethod
    def save():
        db.session.flush()

    def delete(self):
        db.session.delete(self)
        db.session.flush()

    def summary(self, length=150):
        long_field = None

        for field in ('content', 'description'):
            if hasattr(self, field):
                long_field = getattr(self, field)

        if not long_field:
            return ''

        if len(long_field) <= length:
            return long_field

        return truncate_html(long_field, length, end='...')


# Enable all models to be imported from the module. Import at the end to prevent circular imports.
from .category import RedCategory
from .post import RedPost