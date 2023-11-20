from kluster import db

class Roles(db.Model):
    id = db.Column(
        db.String(60)
    )