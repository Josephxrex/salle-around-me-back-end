from datetime import datetime
from app import db

class Style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)
    is_delete = db.Column(db.Boolean, default=False)