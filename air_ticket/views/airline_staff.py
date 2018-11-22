from flask import Blueprint, render_template, request
from air_ticket import conn
from air_ticket.utils import requires_login_airline_staff

mod = Blueprint('airline_staff', __name__, url_prefix='/airline_staff')

# Define route for homepage
@mod.route('/')
@requires_login_airline_staff
def homepage():
	return render_template('airline_staff/index.html')
