from flask import Blueprint, render_template, request, session, redirect
from air_ticket import conn
from air_ticket.utils import requires_login_booking_agent

mod = Blueprint('booking_agent', __name__, url_prefix='/booking_agent')

# Define route for homepage
@mod.route('/')
@requires_login_booking_agent
def homepage():
	return render_template('booking_agent/index.html')

# View my flights
@mod.route('/viewMyFlights', methods=['POST'])
@requires_login_booking_agent
def viewMyFlights():
	# grabs information
	booking_agent_email = session['username']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT ticket_id, customer_email, airline_name, flight_num, airplane_id, 
			departure_airport, departure_time, arrival_airport, arrival_time, 
			status, price, purchase_date
		FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE email = %s AND departure_time > NOW()
		ORDER BY departure_time '''
	cursor.execute(query, (booking_agent_email))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	return render_template('booking_agent/index.html', result=data)

# Purchase tickets
@mod.route('/purchaseTickets', methods=['POST'])
@requires_login_booking_agent
def purchaseTickets():
	# grabs information
	booking_agent_email = session['username']
	customer_email = request.form['customer_email']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']

	# cursor used to send queries
	cursor = conn.cursor()
	# get booking_agent_id
	query = 'SELECT booking_agent_id FROM booking_agent WHERE email = %s'
	cursor.execute(query, (booking_agent_email))
	booking_agent_id = cursor.fetchone()
	# generates ticket_id
	query = 'SELECT COUNT(*) FROM ticket'
	cursor.execute(query)
	count = cursor.fetchone()
	ticket_id = count + 1
	# executes updates
	ins_ticket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
	cursor.execute(ins_ticket, (ticket_id, airline_name, flight_num))
	ins_purchases = 'INSERT INTO purchase VALUES(%s, %s, %s, CURDATE())'
	cursor.execute(ins_purchases, (ticket_id, customer_email, booking_agent_id))
	conn.commit()
	cursor.close()
	return render_template('booking_agent/index.html')	

# Search for flights
@mod.route('/searchFlighs', methods=['POST'])
@requires_login_booking_agent
def searchFlights():
	# grabs information
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	arrival_airport = request.form['arrival_airport']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = ''' 
		SELECT * 
		FROM flight 
		WHERE departure_airport = %s AND DATE(departure_time) = %s AND 
			arrival_airport = %s 
		ORDER BY departure_time '''
	cursor.execute(query, (departure_airport, departure_date, arrival_airport))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	return render_template('booking_agent/index.html', result=data)

# Define route for logout
@mod.route('/logout')
@requires_login_booking_agent
def logout():
	session.pop('username')
	session.pop('usertype')
	session.pop('booking_agent_id')
	return redirect('/')
