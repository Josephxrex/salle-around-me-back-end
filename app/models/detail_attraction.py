from app import db

class detail_attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    size = db.Column(db.String(50))
    tecnique_id = db.Column(db.Integer)
    material_id = db.Column(db.Integer)
    style_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    country_id = db.Column(db.Integer)
    address_id = db.Column(db.Integer)