from flask import Blueprint, render_template, request, session, redirect, url_for
from pymysql import MySQLError
from air_ticket import conn
from air_ticket.utils import requires_login_airline_staff

mod = Blueprint('airline_staff', __name__, url_prefix='/airline_staff')

# Define route for homepage
@mod.route('/')
@requires_login_airline_staff
def homepage():
	return render_template('airline_staff/index.html')

@mod.route('/createNewFlights', methods=['POST'])
@requires_login_airline_staff
def createNewFlights():
	# grabs information
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	departure_airport = request.form['departure_airport']
	departure_time = request.form['departure_time']
	arrival_airport = request.form['arrival_airport']
	arrival_time = request.form['arrival_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']

	try:
		with conn.cursor() as cursor:
			ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(ins, (airline_name, flight_num, departure_airport, departure_time, 
				arrival_airport, arrival_time, price, status, airplane_id))
		conn.commit()
	except MySQLError as e:
		print('Got error {!r}, errno is {}'.format(e, e.args[0]))
	
	return render_template('customer/index.html')

# Change status of flights
@mod.route('/changeFlightStatus', methods=['POST'])
@requires_login_airline_staff
def changeFlightStatus():
	# grabs information
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	status = request.form['status']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		UPDATE flight
		SET status = %s
		WHERE airline_name = %s AND flight_num = %s '''
	cursor.execute(query, (status, airline_name, flight_num))
	# stores the results in a variable
	cursor.close()
	return render_template('customer/index.html')

# Add new airplane
@mod.route('/addNewAirplane', methods=['POST'])
@requires_login_airline_staff
def addNewAirplane():
	# grabs information
	airline_name = session['airline_name']
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']

	try:
		with conn.cursor() as cursor:
			ins = 'INSERT INTO airplane VALUES(%s, %s, %s)'
			cursor.execute(ins, (airline_name, airplane_id, seats))
		conn.commit()
	except MySQLError as e:
		print('Got error {!r}, errno is {}'.format(e, e.args[0]))
	
	return render_template('customer/index.html')

# Add new airport
@mod.route('/addNewAirport', methods=['POST'])
@requires_login_airline_staff
def addNewAirport():
	# grabs information
	airport_name = request.form['airport_name']
	airport_city = request.form['airport_id']

	try:
		with conn.cursor() as cursor:
			ins = 'INSERT INTO airport VALUES(%s, %s)'
			cursor.execute(ins, (airport_name, airport_city))
		conn.commit()
	except MySQLError as e:
		print('Got error {!r}, errno is {}'.format(e, e.args[0]))
	
	return render_template('customer/index.html')

# Define route for logout
@mod.route('/logout')
@requires_login_airline_staff
def logout():
	session.pop('username')
	session.pop('usertype')
	session.pop('airline_name') #TODO
	return redirect('/')
