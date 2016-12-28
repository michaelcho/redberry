from mock import MagicMock, patch

from redberry.tests import RedTestCase
from redberry.models import RedPost, RedCategory


class AdminRoutesTest(RedTestCase):

    @patch('redberry.blueprint.current_user')
    def test_admin_defaults_to_categories(self, mock_user):
        url = "/%s/admin" % self.url_prefix
        categories = RedCategory.query.all()

        response = self.test_client.get(url)
        for category in categories:
            assert category.title in response.data

    @patch('redberry.blueprint.current_user')
    def test_admin_shows_posts(self, mock_user):
        url = "/%s/admin/post" % self.url_prefix
        categories = RedCategory.query.all()

        response = self.test_client.get(url)
        for category in categories:
            assert category.title not in response.data

        posts = RedPost.query.all()
        for post in posts:
            assert post.title in response.data

    @patch('redberry.blueprint.current_user')
    def test_new_record_creates_category(self, mock_user):
        url = "/%s/admin/category/new" % self.url_prefix
        assert RedCategory.query.count() == 1

        response = self.test_client.post(url, data={'title': "A new category"})
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/admin' % self.url_prefix
        self.assert_flashes("Saved category 2", 'success')
        assert RedCategory.query.count() == 2

        new_category = RedCategory.query.all()[-1]
        assert new_category.title == "A new category"

    @patch('redberry.blueprint.current_user')
    def test_new_record_creates_post(self, mock_user):
        url = "/%s/admin/post/new" % self.url_prefix
        assert RedPost.query.count() == 1

        response = self.test_client.post(url, data={'title': "A new post"})
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/admin/post' % self.url_prefix
        self.assert_flashes("Saved post 2", 'success')
        assert RedPost.query.count() == 2

        new_post = RedPost.query.all()[-1]
        assert new_post.title == "A new post"

    @patch('redberry.blueprint.current_user')
    def test_edit_record_updates_category(self, mock_user):
        category = RedCategory.query.first()
        url = "/%s/admin/category/%s" % (self.url_prefix, category.slug)
        assert RedCategory.query.count() == 1

        response = self.test_client.post(url, data={'title': "A new title"})
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/admin' % self.url_prefix
        self.assert_flashes("Saved category 1", 'success')
        assert RedCategory.query.count() == 1
        assert category.title == "A new title"

    @patch('redberry.blueprint.current_user')
    def test_edit_record_updates_post(self, mock_user):
        post = RedPost.query.first()
        url = "/%s/admin/post/%s" % (self.url_prefix, post.slug)
        assert RedPost.query.count() == 1

        response = self.test_client.post(url, data={'title': "A new title"})
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/admin/post' % self.url_prefix
        self.assert_flashes("Saved post 1", 'success')
        assert RedPost.query.count() == 1
        assert post.title == "A new title"

    @patch('redberry.blueprint.current_user')
    def test_edit_record_deletes_category(self, mock_user):
        category = RedCategory.query.first()
        url = "/%s/admin/category/%s" % (self.url_prefix, category.slug)
        assert RedCategory.query.count() == 1

        response = self.test_client.post(url, data={'_method': "DELETE"})
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/admin' % self.url_prefix
        self.assert_flashes("Deleted category", 'success')
        assert RedCategory.query.count() == 0

    @patch('redberry.blueprint.current_user')
    def test_edit_record_deletes_post(self, mock_user):
        post = RedPost.query.first()
        url = "/%s/admin/post/%s" % (self.url_prefix, post.slug)
        assert RedPost.query.count() == 1

        response = self.test_client.post(url, data={'_method': "DELETE"})
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/admin/post' % self.url_prefix
        self.assert_flashes("Deleted post", 'success')
        assert RedPost.query.count() == 0