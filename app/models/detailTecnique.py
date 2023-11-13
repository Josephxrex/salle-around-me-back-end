from app import db

class DetailTecnique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tecnique_id = db.Column(db.Integer)
    attraction_id = db.Column(db.Integer)
    is_delete = db.Column(db.Boolean, default=False)