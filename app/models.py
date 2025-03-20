from app import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(128), nullable=False)
    fabric_type = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), nullable=False, default='Pending')
    date_received = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id} - {self.customer_name}>'

