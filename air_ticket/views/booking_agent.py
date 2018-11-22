from flask import Blueprint, render_template, request
from air_ticket import conn

mod = Blueprint('booking_agent', __name__, url_prefix='/booking_agent')
