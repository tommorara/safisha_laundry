from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import OrderForm
from app.models import Order
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    total_orders = Order.query.count()
    in_progress = Order.query.filter_by(status='In Progress').count()
    completed = Order.query.filter_by(status='Completed').count()
    pending = Order.query.filter_by(status='Pending').count()
    
    return render_template('dashboard.html',
                           total_orders=total_orders,
                           in_progress=in_progress,
                           completed=completed,
                           pending=pending)

@main.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            customer_name=form.customer_name.data,
            fabric_type=form.fabric_type.data,
            quantity=form.quantity.data,
            status=form.status.data,
            date_received=form.date_received.data
        )
        db.session.add(order)
        db.session.commit()
        flash('Order saved successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('form.html', form=form)

@main.route('/report')
def report():
    orders = Order.query.order_by(Order.date_received.desc()).all()
    return render_template('report.html', orders=orders)

