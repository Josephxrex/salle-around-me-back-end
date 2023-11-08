from app import db
class Attraction(db.Model):
    __tablename__ = 'attraction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    img = db.Column(db.String(150))
    id_detail = db.Column(db.Integer, db.ForeignKey('detail_attraction.id'))
    id_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    id_author = db.Column(db.Integer, db.ForeignKey('author.id'))
    id_coordinates = db.Column(db.Integer, db.ForeignKey('coordinates.id'))
    id_mac_address = db.Column(db.Integer, db.ForeignKey('mac_address.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))