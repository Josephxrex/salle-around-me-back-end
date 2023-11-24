from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    father_lastname = db.Column(db.String(60))
    mother_lastname = db.Column(db.String(60))
    birthday = db.Column(db.Date)
    death = db.Column(db.Date)
    is_delete = db.Column(db.Boolean, default=False)