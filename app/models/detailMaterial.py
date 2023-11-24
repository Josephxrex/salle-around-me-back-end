from app import db

class DetailMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    id_attraction = db.Column(db.Integer, db.ForeignKey('attraction.id'))
    is_delete = db.Column(db.Boolean, default=False)