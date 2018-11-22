from flask import Blueprint, render_template, request
from air_ticket import conn

mod = Blueprint('airline_staff', __name__, url_prefix='/airline_staff')