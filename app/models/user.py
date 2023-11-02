from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    password = db.Column(db.String(128))  # Almacena la contraseña hasheada
    token = db.Column(db.String(50))
    email = db.Column(db.String(30))