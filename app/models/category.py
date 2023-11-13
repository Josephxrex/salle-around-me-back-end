from app import db
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.Text)
    is_delete = db.Column(db.Boolean, default=False)