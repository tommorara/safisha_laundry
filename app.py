from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # <-- Added Flask-Migrate support

from models import Order, Fabric

@app.route('/')
def index():
    return render_template('index.html')

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
        status='pending'
    )
    db.session.add(new_order)
    db.session.commit()

    for fabric in data.get('fabrics', []):
        new_fabric = Fabric(
            order_id=new_order.id,
            fabric_type=fabric.get('type'),
            quantity=fabric.get('quantity')
        )
        db.session.add(new_fabric)

    db.session.commit()

    return jsonify({'message': 'Order added successfully'}), 201

@app.route('/get_orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    output = []
    for order in orders:
        fabrics = [{'type': fabric.fabric_type, 'quantity': fabric.quantity} for fabric in order.fabrics]
        output.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'contact_number': order.contact_number,
            'total_weight': order.total_weight,
            'order_received_date': order.order_received_date,
            'due_date': order.due_date,
            'notes': order.notes,
            'status': order.status,
            'fabrics': fabrics
        })
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)

