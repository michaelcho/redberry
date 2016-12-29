import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.testing import TestCase
from flask.ext.login import LoginManager, AnonymousUserMixin


app = Flask(__name__)
db = SQLAlchemy(app, session_options={'autocommit': True, 'expire_on_commit': False})

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = AnonymousUserMixin

url_prefix = 'blog_test'

from redberry.blueprint import cms
app.config['redberry.config'] = {'db': db}
app.register_blueprint(cms, url_prefix="/%s" % url_prefix)


class RedTestCase(TestCase):
    """
    Custom test case class for any common methods.
    """
    def __init__(self, methodName):
        super(RedTestCase, self).__init__(methodName)
        self.test_client = app.test_client()
        self.db = db
        self.logger = logging.getLogger('redberry.tests')
        self.url_prefix = url_prefix

    def create_app(self):
        app.config['SECRET_KEY'] = '8cauliflowers!'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        return app

    def setUp(self):
        from redberry.models.migrate import RedMigrator
        migrator = RedMigrator()
        migrator.initialize_samples()

    def tearDown(self):
        from redberry.models import RedCategory, RedPost
        RedCategory.query.delete()
        RedPost.query.delete()
        self.db.session.execute("DELETE FROM redberry_categories_posts")

    def assert_flashes(self, expected_message, expected_category='message'):
        with self.test_client.session_transaction() as session:
            try:
                category, message = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            assert expected_message in message
            assert expected_category == category
