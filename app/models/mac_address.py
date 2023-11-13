from app import db

class MacAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(17), nullable=False)
    is_delete = db.Column(db.Boolean, default=False)
