from flask import Blueprint, render_template, request
from air_ticket import conn
from air_ticket.utils import requires_login_customer

mod = Blueprint('customer', __name__, url_prefix='/customer')

# Define route for homepage
@mod.route('/')
@requires_login_customer
def homepage():
	return render_template('customer/index.html')
