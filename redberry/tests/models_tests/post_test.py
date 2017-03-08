from redberry.tests import RedTestCase
from redberry.models import RedPost


class RedPostTest(RedTestCase):

    def test_strip_tags(self):
        post = RedPost.query.first()
        assert RedPost.strip_tags(text=post.content) == "A small berry to start the day never hurt anybody."

    def test_keywords(self):
        post = RedPost.query.first()
        assert post.keywords() == 'never, anybody, hurt, start, berry'