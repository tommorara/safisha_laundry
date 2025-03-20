from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    fabric_type = SelectField('Fabric Type', choices=[('Cotton', 'Cotton'), ('Linen', 'Linen'), ('Wool', 'Wool')], validators=[DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], validators=[DataRequired()])
    date_received = DateField('Date Received', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save')

