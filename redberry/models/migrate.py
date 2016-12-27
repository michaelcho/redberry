import logging
from sqlalchemy.sql.elements import quoted_name

from redberry.blueprint import cms
from redberry.models import RedPost, RedCategory
from redberry.models.post import categories_posts


class RedMigrator:

    def __init__(self):
        self.db = cms.config['db']
        self.logger = logging.getLogger('redberry')

    def do_migration(self):
        for model in [RedPost, RedCategory]:
            if not self.db.engine.has_table(quoted_name(model.__table__, True)):
                self.logger.warning("Creating database table %s" % model.__tablename__)
                model.__table__.create(self.db.engine)

        if not self.db.engine.has_table(categories_posts.name):
            self.logger.warning("Creating database join table %s" % categories_posts.name)
            categories_posts.create(self.db.engine)

    def initialize_samples(self):
        if not RedCategory.query.count():
            self.logger.info("Inserting sample category")
            category = RedCategory(title="Tips & Tricks", description="A few posts for working with Redberry")
            self.db.session.add(category)

        if not RedPost.query.count():
            self.logger.info("Inserting sample post")
            post = RedPost(title="Berries, berries everywhere!", content="A small berry to start the day never hurt anybody.")
            post.categories = [RedCategory.query.first()]
            self.db.session.add(post)

        self.db.session.flush()
