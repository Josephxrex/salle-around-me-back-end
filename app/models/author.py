from app import db

class Author(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  lastname = db.Column(db.String(60))
  birthday = db.Column(db.DateTime)
  death = db.Column(db.DateTime)
  description = db.Column(db.String(200))
  img = db.Column(db.String(150))