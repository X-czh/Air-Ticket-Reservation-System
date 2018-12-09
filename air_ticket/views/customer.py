from flask import Blueprint, render_template, request, session, redirect
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from air_ticket import conn
from air_ticket.utils import requires_login_customer

mod = Blueprint('customer', __name__, url_prefix='/customer')


# Define route for homepage
@mod.route('/')
@requires_login_customer
def homepage():
	return render_template('customer/index.html')


# View my flights
@mod.route('/viewMyFlights', methods=['POST'])
@requires_login_customer
def viewMyFlights():
	# grabs information
	customer_email = session['username']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT *
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND departure_time > NOW()
		ORDER BY departure_time '''
	cursor.execute(query, (customer_email))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()

	# check data
	if data:
		return render_template('customer/index.html', result_viewMyFlights=data)
	else:
		msg = 'No records are found!'
		return render_template('customer/index.html', message_viewMyFlights=msg)


# View my flights option
@mod.route('/viewMyFlightsOption', methods=['POST'])
@requires_login_customer
def viewMyFlightsOption():
	# grabs information
	customer_email = session['username']
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
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND DATE(departure_time) BETWEEN %s AND %s '''
	cursor.execute(query, (customer_email, start_date, end_date))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()

	# check data
	if data:
		return render_template('customer/index.html', result_viewMyFlights=data)
	else:
		msg = 'No records are found!'
		return render_template('customer/index.html', message_viewMyFlights=msg)


# Purchase tickets
@mod.route('/purchaseTickets', methods=['POST'])
@requires_login_customer
def purchaseTickets():
	# grabs information
	customer_email = session['username']
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
		ins_purchases = 'INSERT INTO purchases VALUES(%s, %s, NULL, CURDATE())'
		cursor.execute(ins_purchases, (ticket_id, customer_email))
		conn.commit()
	else:
		msg = 'All tickets have been sold out!'

	cursor.close()
	return render_template('customer/index.html', message_purchaseTickets=msg)


# Search for flights
@mod.route('/searchFlights', methods=['POST'])
@requires_login_customer
def searchFlights():
	# grabs information
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	arrival_airport = request.form['arrival_airport']
	arrival_date = request.form['arrival_date']

	# check consistence of dates
	if departure_date > arrival_date:
		error = 'Error: arrival date is earlier than departure date!'
		return render_template('customer/index.html', message_searchFlights=error)
	
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
		return render_template('customer/index.html', result_searchFlights=data)
	else:
		msg = 'No records are found!'
		return render_template('customer/index.html', message_searchFlights=msg)


# Track my spending default view
@mod.route('/trackMySpendingDefault', methods=['POST'])
@requires_login_customer
def trackMySpendingDefault():
	# grabs information
	customer_email = session['username']

	# computes date
	end_date = (date.today() + relativedelta(months=+1)).replace(day=1)
	end_date_str = end_date.strftime('%Y-%m-%d')
	start_date = end_date - relativedelta(months=+6)
	start_date_str = start_date.strftime('%Y-%m-%d')

	# cursor used to send queries
	cursor = conn.cursor()
	# query
	query = ''' 
		SELECT SUM(price) as total
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND purchase_date >= %s AND purchase_date < %s'''
	
	# total
	cursor.execute(query, (customer_email, start_date_str, end_date_str))
	data = cursor.fetchone()
	total = data['total'] if data['total'] != None else 0

	# monthwise
	monthwise_label = []
	monthwise_total = []
	end_date = start_date + relativedelta(months=+1)
	for _ in range(6):
		start_date_str = start_date.strftime('%Y-%m-%d')
		end_date_str = end_date.strftime('%Y-%m-%d')
		cursor.execute(query, (customer_email, start_date_str, end_date_str))
		monthwise = cursor.fetchone()
		monthwise_label.append(start_date.strftime('%y/%m'))
		monthwise_total.append(monthwise['total'] if monthwise['total'] != None else 0)
		start_date += relativedelta(months=+1)
		end_date += relativedelta(months=+1)

	cursor.close()
	return render_template('customer/index.html', total=total, 
		monthwise_label=monthwise_label, monthwise_total=monthwise_total)


# Track my spending optional view
@mod.route('/trackMySpendingOptional', methods=['POST'])
@requires_login_customer
def trackMySpendingOptional():
	# grabs information
	customer_email = session['username']
	start_month = request.form['start_month']
	end_month = request.form['end_month']

	# check consistence of months
	if start_month > end_month:
		error = 'Error: end month is earlier than start month!'
		return render_template('customer/index.html', message_trackMySpendingOptional=error)

	# computes date
	start_date = datetime.strptime(start_month, '%Y-%m').date()
	start_date_str = start_date.strftime('%Y-%m-%d')
	end_date = datetime.strptime(end_month, '%Y-%m').date() + relativedelta(months=+1)
	end_date_str = end_date.strftime('%Y-%m-%d')
	diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

	# cursor used to send queries
	cursor = conn.cursor()
	# query
	query = ''' 
		SELECT SUM(price) as total
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND purchase_date >= %s AND purchase_date < %s'''
	
	# total
	cursor.execute(query, (customer_email, start_date_str, end_date_str))
	data = cursor.fetchone()
	total = data['total'] if data['total'] != None else 0

	# monthwise
	monthwise_label = []
	monthwise_total = []
	end_date = start_date + relativedelta(months=+1)
	for _ in range(diff):
		start_date_str = start_date.strftime('%Y-%m-%d')
		end_date_str = end_date.strftime('%Y-%m-%d')
		cursor.execute(query, (customer_email, start_date_str, end_date_str))
		monthwise = cursor.fetchone()
		monthwise_label.append(start_date.strftime('%y/%m'))
		monthwise_total.append(monthwise['total'] if monthwise['total'] != None else 0)
		start_date += relativedelta(months=+1)
		end_date += relativedelta(months=+1)

	cursor.close()
	return render_template('customer/index.html', total_option=total, 
		monthwise_label_option=monthwise_label, monthwise_total_option=monthwise_total)


# Define route for logout
@mod.route('/logout')
@requires_login_customer
def logout():
	session.pop('username')
	session.pop('usertype')
	return redirect('/')
