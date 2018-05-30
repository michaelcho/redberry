
def upgrade(db):
    db.session.execute("ALTER TABLE redberry_posts ADD hero_image TEXT AFTER summary")

def downgrade(db):
    db.session.execute("ALTER TABLE redberry_posts DROP hero_image")