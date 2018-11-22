from flask import Blueprint, render_template, request
from air_ticket import conn
from air_ticket.utils import requires_login_booking_agent

mod = Blueprint('booking_agent', __name__, url_prefix='/booking_agent')

# Define route for homepage
@mod.route('/')
@requires_login_booking_agent
def homepage():
	return render_template('booking_agent/index.html')
