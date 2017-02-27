import logging
from sqlalchemy.sql.elements import quoted_name
import importlib

from redberry.blueprint import cms
from redberry.models import RedPost, RedCategory, RedVersion
from redberry.models.post import categories_posts


class RedMigrator:

    def __init__(self):
        self.db = cms.config['db']
        self.logger = logging.getLogger('redberry')

    def do_migration(self):
        for model in [RedVersion, RedPost, RedCategory]:
            if not self.db.engine.has_table(quoted_name(model.__table__, True)):
                self.logger.warning("Creating database table %s" % model.__tablename__)
                model.__table__.create(self.db.engine)

        if not self.db.engine.has_table(categories_posts.name):
            self.logger.warning("Creating database join table %s" % categories_posts.name)
            categories_posts.create(self.db.engine)

        # Run migrations
        migrations = RedVersion.all_migrations()
        self.logger.warning("--- Migrations %s" % migrations)

        # Migrations ['201612311100_add_publish_state.py', '201612311300_dummy.py']
        for migration in migrations:
            migration_file = migration.split(".")[0]  # eg "201612311100_add_publish_state"
            self.run_migration(migration_file=migration_file)

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

    def run_migration(self, migration_file, method='upgrade'):

        if RedVersion.already_run(migration_file):
            self.logger.warn("Migration %s has already been run, skipping." % migration_file)
            return

        try:
            module = importlib.import_module('redberry.models.migrations.%s' % migration_file)

            if method == 'upgrade':
                self.logger.info("Running upgrade on %s" % migration_file)
                module.upgrade(self.db)
            else:
                self.logger.info("Running downgrade on %s" % migration_file)
                module.downgrade(self.db)

            RedVersion.store_migration(migration_file)

        except Exception, e:
            self.logger.error("Error running %s" % migration_file)
            self.logger.error(e)

