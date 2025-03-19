from flask import Blueprint, request, jsonify
from .models import db, Order

main = Blueprint('main', __name__)

@main.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        type_of_clothes=data['type_of_clothes'],
        quantity=data['quantity'],
        date_received=data['date_received'],
        date_to_be_collected=data['date_to_be_collected'],
        status=data['status']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@main.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = [{'id': o.id, 'type_of_clothes': o.type_of_clothes, 'quantity': o.quantity,
               'date_received': o.date_received, 'date_to_be_collected': o.date_to_be_collected,
               'status': o.status} for o in orders]
    return jsonify(result)

@main.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

