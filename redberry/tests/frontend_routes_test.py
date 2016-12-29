from redberry.tests import RedTestCase
from redberry.models import RedPost, RedCategory


class FrontendRoutesTest(RedTestCase):

    def test_home(self):
        url = '/%s/' % self.url_prefix
        response = self.test_client.get(url)

        # Shows published
        post = RedPost.query.first()
        assert post.title in response.data
        assert post.content in response.data

        # Does not show if not published
        post.published = False
        response = self.test_client.get(url)
        assert post.title not in response.data
        assert post.content not in response.data
        assert "No posts yet." in response.data

    def test_show_post(self):
        post = RedPost.query.first()
        url = "/%s/%s" % (self.url_prefix, post.slug)

        # Shows by slug
        response = self.test_client.get(url)
        assert post.title in response.data
        assert post.content in response.data

        # Redirects if invalid slug
        response = self.test_client.get(url + "-invalid")
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/' % self.url_prefix
        self.assert_flashes("Post not found!", 'danger')

    def test_show_category(self):
        category = RedCategory.query.first()
        url = "/%s/category/%s" % (self.url_prefix, category.slug)

        # Shows by slug
        response = self.test_client.get(url)
        assert category.title in response.data
        assert category.description in response.data

        # Shows category posts
        if category.posts:
            assert category.posts[0].title in response.data

        # Redirects if invalid slug
        response = self.test_client.get(url + "-invalid")
        assert response.status_code == 302
        assert response.location == 'http://localhost/%s/' % self.url_prefix
        self.assert_flashes("Category not found!", 'danger')

