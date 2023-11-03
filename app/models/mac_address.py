from app import db


class MacAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(20))
