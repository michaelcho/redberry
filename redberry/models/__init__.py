from slugify import slugify
from html5lib_truncation import truncate_html
from bs4 import BeautifulSoup
import re
from string import punctuation as p

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

    @staticmethod
    def strip_tags(text, strip_punctuation=False):
        # Return only the words from content, stripping punctuation and HTML.
        soup = BeautifulSoup(text)

        if strip_punctuation:
            punctuation = re.compile('[{}]+'.format(re.escape(p)))
            words_only = punctuation.sub('', soup.get_text())
            return words_only

        words_only = soup.get_text()
        return words_only

    def summarise(self, length=150):
        long_field = None

        if hasattr(self, 'summary'):
            long_field = getattr(self, 'summary')

        if not long_field:
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
from .version import RedVersion