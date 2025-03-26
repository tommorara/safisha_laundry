from flask import Blueprint, request, render_template, jsonify
from datetime import datetime
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

    if status == 'active':
        orders = Order.query.filter(Order.status != 'finished').all()
    elif status == 'finished':
        orders = Order.query.filter_by(status='picked-up').all()
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

