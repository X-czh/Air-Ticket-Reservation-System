from flask import Blueprint, render_template, request
from air_ticket import conn

mod = Blueprint('customer', __name__, url_prefix='/customer')