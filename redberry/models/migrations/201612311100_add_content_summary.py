
def upgrade(db):
    db.session.execute("ALTER TABLE redberry_posts ADD summary TEXT AFTER content")

def downgrade(db):
    db.session.execute("ALTER TABLE redberry_posts DROP summary")