from redberry.tests import RedTestCase
from redberry.models import RedPost, RedCategory


class BlueprintTest(RedTestCase):

    def test_init_redberry_creates_samples(self):
        assert RedPost.query.count() >= 1
        assert RedCategory.query.count() >= 1
