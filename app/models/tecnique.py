from app import db


class Tecnique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    is_delete = db.Column(db.Boolean, default=False)
