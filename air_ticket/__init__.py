# Initialize the app from Flask
from flask import Flask
app = Flask(__name__)
app.secret_key = 'some key that you will never guess'

# Configure MySQL
import pymysql.cursors
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='password',
                       db='air_ticket',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Register blueprints
from air_ticket.views import general, customer, booking_agent, airline_staff
app.register_blueprint(general.mod)
app.register_blueprint(customer.mod)
app.register_blueprint(booking_agent.mod)
app.register_blueprint(airline_staff.mod)
