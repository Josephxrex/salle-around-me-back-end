from app import db
import datetime



class Tecnique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    is_delete = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.TIMESTAMP,
                          default=datetime.datetime.utcnow)
    update_at = db.Column(db.TIMESTAMP,
                          default=datetime.datetime.utcnow)

