from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from datetime import datetime, date
from app.models import db, Order, Fabric
import random

main = Blueprint('main', __name__)

# 🔢 Generate a unique random order number between 1000–5000
def generate_unique_order_number(min_val=1000, max_val=5000):
    existing = {o.order_number for o in Order.query.with_entities(Order.order_number).all()}
    possible = set(range(min_val, max_val + 1)) - existing
    if not possible:
        raise ValueError("No more unique order numbers available.")
    return random.choice(list(possible))

# 🏠 Home Page
@main.route('/')
def index():
    return render_template('index.html')

# 🧾 Order Form Page
@main.route('/create')
def create_order_page():
    return render_template('create_order.html')

# 📜 List All Orders (debug view)
@main.route('/orders')
def all_orders():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

# 📦 Filter Orders by Status
@main.route('/<status>')
def get_orders_by_status(status):
    valid_statuses = ['pending', 'active', 'processed', 'cancelled', 'overdue', 'finished']
    if status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 404

    # 🔄 Auto-mark overdue
    overdue_orders = Order.query.filter(
        Order.due_date < date.today(),
        Order.status.notin_(['finished', 'cancelled', 'overdue'])
    ).all()
    for order in overdue_orders:
        order.status = 'overdue'
    db.session.commit()

    orders = Order.query.filter_by(status=status).all()
    return render_template(f"{status}.html", orders=orders)

# 📤 Add Order API
@main.route('/add_order', methods=['POST'])
def add_order():
    try:
        data = request.get_json(force=True)
        print("📥 Received order data:", data)

        required_fields = ['customer_name', 'contact_number', 'order_received_date', 'due_date', 'fabrics']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        new_order = Order(
            order_number=generate_unique_order_number(),
            customer_name=data['customer_name'],
            contact_number=data['contact_number'],
            total_weight=float(data.get('total_weight', 0)),
            order_received_date=datetime.strptime(data['order_received_date'], "%Y-%m-%d"),
            due_date=datetime.strptime(data['due_date'], "%Y-%m-%d"),
            notes=data.get('notes'),
            status='pending'
        )
        db.session.add(new_order)
        db.session.commit()

        for fabric in data['fabrics']:
            db.session.add(Fabric(
                order_id=new_order.id,
                fabric_type=fabric['type'],
                quantity=int(fabric['quantity'])
            ))
        db.session.commit()

        return jsonify({
            "message": "Order added successfully",
            "order_number": new_order.order_number
        }), 201

    except Exception as e:
        db.session.rollback()
        print("❌ Error while adding order:", str(e))
        return jsonify({"error": str(e)}), 500

# 🔁 Update Order Status
@main.route('/update_status/<int:order_id>', methods=['POST', 'PATCH'])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status') or request.json.get('status')

    transitions = {
        'pending': ['active', 'cancelled'],
        'active': ['processed', 'cancelled'],
        'processed': ['finished', 'cancelled'],
        'cancelled': [],
        'finished': [],
        'overdue': []
    }

    if new_status in transitions.get(order.status, []):
        order.status = new_status
        db.session.commit()
        if request.is_json:
            return jsonify({'message': f'Status updated to {new_status}'}), 200
        else:
            return redirect(request.referrer or url_for('main.index'))
    else:
        return jsonify({'error': f"Invalid transition from {order.status} to {new_status}"}), 400

# 🎽 Provide fabric type list to frontend dynamically
@main.route('/fabric_types')
def get_fabric_types():
    return jsonify([
        'Trouser', 'Shirt', 'Suit', 'Coat', 'Dress',
        'Skirt', 'Blouse', 'Jacket', 'Kitenge', 'Sweater', 'Others'
    ])

