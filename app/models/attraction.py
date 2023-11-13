from app import db

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    description = db.Column(db.Text)
    img = db.Column(db.JSON)
    size = db.Column(db.Integer)
    id_author = db.Column(db.Integer)
    id_style = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    id_mac_address = db.Column(db.Integer)
    id_category = db.Column(db.Integer)
    is_delete = db.Column(db.Boolean, default=False)