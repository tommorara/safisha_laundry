from . import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    total_weight = db.Column(db.Float)
    order_received_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    fabrics = db.relationship('Fabric', backref='order', lazy=True)

class Fabric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    fabric_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

