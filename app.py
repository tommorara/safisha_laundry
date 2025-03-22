from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

# ✅ Initialize Flask and Config
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# ✅ Models
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    total_weight = db.Column(db.Float, nullable=True)
    order_received_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')

    fabrics = db.relationship('Fabric', backref='order', lazy=True)

class Fabric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    fabric_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# ✅ Render Dashboard
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Create Order Page Route
@app.route('/create')
def create_order_page():
    return render_template('create_order.html')

# ✅ General Route for Orders Based on Status
@app.route('/<status>')
def get_orders(status):
    valid_statuses = ['pending', 'active', 'processed', 'cancelled', 'overdue', 'finished']
    
    if status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 404
    
    if status == 'active':
        orders = Order.query.filter(Order.status != 'finished').all()
    elif status == 'finished':
        orders = Order.query.filter_by(status='picked-up').all()
    else:
        orders = Order.query.filter_by(status=status).all()
    
    return render_template(f'{status}.html', orders=orders)

# ✅ Create a New Order
@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(
        customer_name=data.get('customer_name'),
        contact_number=data.get('contact_number'),
        total_weight=data.get('total_weight'),
        order_received_date=data.get('order_received_date'),
        due_date=data.get('due_date'),
        notes=data.get('notes'),
        status='pending'  # Automatically set to Pending
    )
    db.session.add(new_order)
    db.session.commit()

    # ✅ Add fabrics linked to the order
    for fabric in data.get('fabrics', []):
        new_fabric = Fabric(
            order_id=new_order.id,
            fabric_type=fabric.get('type'),
            quantity=fabric.get('quantity')
        )
        db.session.add(new_fabric)

    db.session.commit()
    return jsonify({'message': 'Order added successfully'}), 201

# ✅ Update an Existing Order
@app.route('/update_order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json

    order.customer_name = data.get('customer_name', order.customer_name)
    order.contact_number = data.get('contact_number', order.contact_number)
    order.total_weight = data.get('total_weight', order.total_weight)
    order.order_received_date = data.get('order_received_date', order.order_received_date)
    order.due_date = data.get('due_date', order.due_date)
    order.notes = data.get('notes', order.notes)

    # ✅ Delete old fabrics and replace them with new ones
    Fabric.query.filter_by(order_id=order.id).delete()
    for fabric in data.get('fabrics', []):
        new_fabric = Fabric(
            order_id=order.id,
            fabric_type=fabric.get('type'),
            quantity=fabric.get('quantity')
        )
        db.session.add(new_fabric)

    db.session.commit()
    return jsonify({'message': 'Order updated successfully'}), 200

# ✅ Delete an Order
@app.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200

# ✅ Update the Status of an Order
@app.route('/update_status/<int:order_id>', methods=['PATCH'])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'message': 'Status updated successfully'}), 200

# ✅ Restore a Cancelled Order to Pending
@app.route('/restore_order/<int:order_id>', methods=['PATCH'])
def restore_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'pending'
    db.session.commit()
    return jsonify({'message': 'Order restored to pending'}), 200

# ✅ Initialize Database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

