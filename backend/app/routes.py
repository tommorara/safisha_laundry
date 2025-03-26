from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from datetime import datetime, date
from app.models import db, Order, Fabric

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/create')
def create_order_page():
    return render_template('create_order.html')


@main.route('/<status>')
def get_orders_by_status(status):
    valid_statuses = ['pending', 'active', 'processed', 'cancelled', 'overdue', 'finished']
    if status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 404

    # 🔄 Auto-mark overdue orders
    overdue_orders = Order.query.filter(
        Order.due_date < date.today(),
        Order.status.notin_(['finished', 'cancelled', 'overdue'])
    ).all()
    for order in overdue_orders:
        order.status = 'overdue'
    db.session.commit()

    # 🧠 Filter by status
    if status == 'active':
        orders = Order.query.filter(Order.status == 'active').all()
    else:
        orders = Order.query.filter_by(status=status).all()

    return render_template(f"{status}.html", orders=orders)


@main.route('/add_order', methods=['POST'])
def add_order():
    try:
        data = request.json
        new_order = Order(
            customer_name=data['customer_name'],
            contact_number=data['contact_number'],
            total_weight=data.get('total_weight', 0),
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
                quantity=fabric['quantity']
            ))
        db.session.commit()

        return jsonify({"message": "Order added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main.route('/update_status/<int:order_id>', methods=['POST', 'PATCH'])
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status') or request.json.get('status')

    # ✅ Updated transition logic
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
        error_msg = f"Invalid transition from {order.status} to {new_status}"
        return jsonify({'error': error_msg}), 400

