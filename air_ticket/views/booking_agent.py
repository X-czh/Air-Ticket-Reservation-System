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
		SELECT *
		FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE email = %s AND departure_time > NOW()
		ORDER BY departure_time '''
	cursor.execute(query, (booking_agent_email))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()

	# check data
	if data:
		return render_template('booking_agent/index.html', result_viewMyFlights=data)
	else:
		msg = 'No records are found!'
		return render_template('booking_agent/index.html', message_viewMyFlights=msg)


# View my flights option
@mod.route('/viewMyFlightsOption', methods=['POST'])
@requires_login_booking_agent
def viewMyFlightsOption():
	# grabs information
	booking_agent_email = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	
	# check consistence of dates
	if start_date > end_date:
		error = 'Error: end date is earlier than start date!'
		return render_template('customer/index.html', message_viewMyFlights=error)

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT *
		FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE email = %s AND DATE(departure_time) BETWEEN %s AND %s '''
	cursor.execute(query, (booking_agent_email, start_date, end_date))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()

	# check data
	if data:
		return render_template('booking_agent/index.html', result_viewMyFlights=data)
	else:
		msg = 'No records are found!'
		return render_template('booking_agent/index.html', message_viewMyFlights=msg)


# Purchase tickets
@mod.route('/purchaseTickets', methods=['POST'])
@requires_login_booking_agent
def purchaseTickets():
	# grabs information
	booking_agent_id = session['booking_agent_id']
	customer_email = request.form['customer_email']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']

	# cursor used to send queries
	cursor = conn.cursor()
	
	# check seat availability
	query = '''
		SELECT COUNT(*) as count, seats
		FROM ticket NATURAL JOIN flight NATURAL JOIN airplane
		WHERE airline_name = %s AND flight_num = %s
		GROUP BY airline_name, flight_num '''
	cursor.execute(query, (airline_name, flight_num))
	data = cursor.fetchone()
	if data['count'] < data['seats']:
		msg = "Purchase successful!"
		# generates ticket_id
		query = 'SELECT COUNT(*) as count FROM ticket'
		cursor.execute(query)
		data = cursor.fetchone()
		ticket_id = data['count'] + 1
		# executes updates
		ins_ticket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
		cursor.execute(ins_ticket, (ticket_id, airline_name, flight_num))
		ins_purchases = 'INSERT INTO purchases VALUES(%s, %s, %s, CURDATE())'
		cursor.execute(ins_purchases, (ticket_id, customer_email, booking_agent_id))
		conn.commit()
	else:
		msg = 'All tickets have been sold out!'

	cursor.close()
	return render_template('booking_agent/index.html', message=msg)	


# Search for flights
@mod.route('/searchFlights', methods=['POST'])
@requires_login_booking_agent
def searchFlights():
	# grabs information
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	arrival_airport = request.form['arrival_airport']
	arrival_date = request.form['arrival_date']

	# check consistence of dates
	if departure_date > arrival_date:
		error = 'Error: arrival date is earlier than departure date!'
		return render_template('booking_agent/index.html', message_searchFlights=error)

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT * 
		FROM flight 
		WHERE departure_airport = %s AND DATE(departure_time) = %s AND 
			arrival_airport = %s AND DATE(arrival_time) = %s '''
	cursor.execute(query, (departure_airport, departure_date, arrival_airport, arrival_date))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	
	# check data
	if data:
		return render_template('booking_agent/index.html', result_searchFlights=data)
	else:
		msg = 'No records are found!'
		return render_template('booking_agent/index.html', message_searchFlights=msg)


# View my commission - default
@mod.route('/commission_default', methods=['POST'])
@requires_login_booking_agent
def commission_default():
	# grabs information
	booking_agent_id = session['booking_agent_id']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT 
			SUM(price) * 0.1 as sum_commission, 
			AVG(price) * 0.1 as avg_commission, 
			COUNT(*) as num_tickets
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE booking_agent_id = %s AND 
			purchase_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH) '''
	cursor.execute(query, (booking_agent_id))
	# stores the results in a variable
	data = cursor.fetchone()
	cursor.close()
	
	# check data
	if data['num_tickets'] > 0:
		return render_template('booking_agent/index.html', result_commission_default=data)
	else:
		msg = 'You did not sell any tickets in the period!'
		return render_template('booking_agent/index.html', message_commission=msg)


# View my commission - option
@mod.route('/commission_option', methods=['POST'])
@requires_login_booking_agent
def commission_option():
	# grabs information
	booking_agent_id = session['booking_agent_id']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# check consistence of dates
	if start_date > end_date:
		error = 'Error: start date is earlier than end date!'
		return render_template('general/index.html', message_commission=error)
	
	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT 
			SUM(price) * 0.1 as sum_commission, 
			AVG(price) * 0.1 as avg_commission, 
			COUNT(*) as num_tickets
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE booking_agent_id = %s AND 
			purchase_date BETWEEN %s AND %s '''
	cursor.execute(query, (booking_agent_id, start_date, end_date))
	# stores the results in a variable
	data = cursor.fetchone()
	cursor.close()

	# check data
	if data['num_tickets'] > 0:
		return render_template('booking_agent/index.html', result_commission_option=data)
	else:
		msg = 'You did not sell any tickets in the period!'
		return render_template('booking_agent/index.html', message_commission=msg)


# View top customers
@mod.route('/viewTopCustomers', methods=['POST'])
@requires_login_booking_agent
def viewTopCustomers():
	# grabs information
	booking_agent_id = session['booking_agent_id']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = ''' 
		SELECT customer_email, COUNT(*) as count
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE booking_agent_id = %s AND 
			purchase_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
		GROUP BY customer_email
		ORDER BY count DESC 
		LIMIT 5 '''
	cursor.execute(query, (booking_agent_id))
	top5_by_count = cursor.fetchall()
	query = ''' 
		SELECT customer_email, SUM(price) * 0.1 as commission
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE booking_agent_id = %s AND 
			purchase_date >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
		GROUP BY customer_email
		ORDER BY commission DESC 
		LIMIT 5 '''
	cursor.execute(query, (booking_agent_id))
	top5_by_commission = cursor.fetchall()
	cursor.close()

	# check status
	msg = None
	if top5_by_commission != None:
		msg = 'No records in the last year!'
	elif top5_by_count != None:
		msg = 'No records in the last 6 months!'
	return render_template('booking_agent/index.html',	
		top5_by_count=top5_by_count,
		top5_by_commission=top5_by_commission,
		message_viewTopCustomers=msg)


# Define route for logout
@mod.route('/logout')
@requires_login_booking_agent
def logout():
	session.pop('username')
	session.pop('usertype')
	session.pop('booking_agent_id')
	return redirect('/')
