from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_clothes = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_received = db.Column(db.Date)
    date_to_be_collected = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False)

